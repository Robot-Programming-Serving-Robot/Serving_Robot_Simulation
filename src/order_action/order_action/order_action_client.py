import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from action_interfaces.action import Order

class OrderActionClient(Node):

    def __init__(self):
        super().__init__('order_action_client')
        self._action_client = ActionClient(self, Order, 'order')

    def send_goal(self, order):
        goal_msg = Order.Goal()
        goal_msg.orders = order
        
        self._action_client.wait_for_server()

        return self._action_client.send_goal_async(goal_msg)
    
def main(args=None):
    rclpy.init(args=args)

    action_client = OrderActionClient()

    
    future = action_client.send_goal([1, 2, 3, 4]) #1,2 주방, 3,4 좌석 서빙

    rclpy.spin_until_future_complete(action_client, future)
    

if __name__ == '__main__':
    main()