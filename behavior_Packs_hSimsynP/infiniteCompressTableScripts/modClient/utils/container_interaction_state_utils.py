# -*- coding: utf-8 -*-


class NodeId(object):
    Idle = 1
    SelectSlot = 2
    UnSelectSlot = 3
    Swap = 4
    TouchProgressiveSelect = 5
    TouchProgressiveSelectComplete = 6
    TouchProgressiveSelectCancel = 7
    DropAll = 8
    Coalesce = 9


class ButtonEventType(object):
    Clicked = 0
    Pressed = 1
    Released = 2
    DoubleClick = 3


class Node(object):
    def __init__(self, on_enter, on_exit):
        super(Node, self).__init__()
        self.mOnEnter = on_enter
        self.mOnExit = on_exit

    def on_enter(self, button_path):
        if self.mOnEnter:
            self.mOnEnter(button_path)

    def on_exit(self, button_path):
        if self.mOnExit:
            self.mOnExit(button_path)


class ButtonEdge(object):
    def __init__(self, target, requirement, priority):
        super(ButtonEdge, self).__init__()
        self.mRequirement = requirement
        self.mTargetNodeId = target
        self.mPriority = priority

    def requirement(self, button_path, button_event_type):
        if self.mRequirement:
            return self.mRequirement(button_path, button_event_type)
        return False

    def get_target_node_id(self):
        return self.mTargetNodeId

    def get_priority(self):
        return self.mPriority


class ContainerInteractionStateMachine(object):
    def __init__(self):
        super(ContainerInteractionStateMachine, self).__init__()
        self.current_node = None
        self.current_node_id = None
        self.default_node_id = NodeId.Idle
        self.nodes = {}
        self.button_edges = {}

    def add_node(self, node_id, on_enter=None, on_exit=None, default_node=False):
        if self.nodes.get(node_id) is not None:
            print "{0} Node with the same name already exists in the state machine!".format(node_id)
            return
        node = Node(on_enter, on_exit)
        self.nodes[node_id] = node
        self.button_edges[node_id] = []
        if default_node or self.current_node_id is None:
            self.current_node = node
            self.current_node_id = node_id
            self.default_node_id = node_id

    def add_edge(self, source, target, requirement=None, priority=0):
        edges = self.button_edges.get(source)
        if not isinstance(edges, list):
            print "there is no node named {0}".format(source)
            return
        target_index = -1
        for i in range(len(edges)):
            if edges[i].get_priority() < priority:
                target_index = i
        if target_index == -1:
            edges.append(ButtonEdge(target, requirement, priority))
        else:
            edges.insert(target_index, ButtonEdge(target, requirement, priority))

    def receive_event(self, button_path, button_event_type):
        edges = self.button_edges.get(self.current_node_id)
        if edges:
            for edge in edges:
                if edge.requirement(button_path, button_event_type):
                    self.change_state(edge.get_target_node_id(), button_path)
                    break

    def reset_to_default(self):
        if self.current_node_id != self.default_node_id:
            self.change_state(self.default_node_id)

    def change_state(self, target, button_path=None):
        node = self.nodes.get(target)
        if not node:
            print "Tried to change to a none existent state!"
        self.current_node.on_exit(button_path)
        self.current_node_id = target
        self.current_node = self.nodes[target]
        self.current_node.on_enter(button_path)

    def get_current_node_id(self):
        return self.current_node_id
