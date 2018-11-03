class Store:
    def __init__(self, initial_state):
        self.state = initial_state
        self.subscribers = []

    def dispatch(self, action):
        print(repr(action))

        new_state = action(self.state)

        for subscriber in self.subscribers:
            subscriber(self.state, new_state)

        self.state = new_state
        return new_state

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
