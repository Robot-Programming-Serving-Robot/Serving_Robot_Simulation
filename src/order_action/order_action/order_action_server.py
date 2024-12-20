import rclpy
from rclpy.action import ActionServer
from rclpy.action import ActionClient
from rclpy.node import Node
from action_interfaces.action import Order #order action interface
from nav2_msgs.action import NavigateToPose


class OrderActionServer(Node):

    def __init__(self):
        super().__init__('order_action_server')
        self._action_server = ActionServer(
            self,
            Order,
            'order',
            self.start_serving_callback)
        
        self._nav_client = ActionClient( #navigate_to_pose 클라이언트
            self,
            NavigateToPose,
            'navigate_to_pose')
        
        # 음식 수령 지점
        self._dic_kitchen = {1: [1., 4., 3.15],
                              2: [1., 3., 3.15], 
                              3: [1., 2., 3.15],
                              4: [1., 1., 3.15]}
        
        # 서빙 테이블 지점
        self._dic_table = {1: [0., -2., 3.15],
                            2: [2., 2., 0.], 
                            3: [2., 0., 0.],
                            4: [5., 2., 0.],
                            5: [5., 0., 0.],
                            6: [8.5, 1., -0.25]}
        
        # 수령 지점 번호와 대응되는 메뉴
        self._dic_food = {1: "Americano", 2: "Espresso", 3: "Decaf", 4: "Latte"}

    
    def send_point(self, x, y, theta):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map" 
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.z = theta
        #_nav_client에서 navigate_to_pose 메시지로 send_goal
        self._nav_client.wait_for_server()
        self._nav_client.send_goal_async(goal_msg)
        
    #액션 호출시 콜백되는 함수
    def start_serving_callback(self, goal_handle):
        self.get_logger().info('Serving the order now...')
        result = Order.Result()
        result.is_success = False

        goal = goal_handle.request.orders #Order 인터페이스 goal값 받아옴
        feedback_msg = Order.Feedback() 
        #order_action의 피드백 메시지 퍼블리시, 출력
        feedback_msg.remain_points = goal 
        self.get_logger().info('Feedback remain points: {0}'.format(feedback_msg.remain_points)) 
        goal_handle.publish_feedback(feedback_msg)
        
        count_pnts = 0 #지나온 지점 인덱스 count
        for i in goal[0:int(len(goal)/2)]: #주방 지점 (전체 인수의 절반)
            self.send_point(self._dic_kitchen[i][0], #주방 딕셔너리에 저장된 좌표로 send_point 인수 대입
                            self._dic_kitchen[i][1],
                            self._dic_kitchen[i][2]) 
            input()
            print(f"Received {self._dic_food[i]}") #메뉴 딕셔너리에 해당하는 메뉴 출력
            count_pnts += 1
            #order_action의 피드백 메시지 퍼블리시, 출력
            feedback_msg.remain_points = goal[count_pnts:int(len(goal))]
            self.get_logger().info('Feedback remain points: {0}'.format(feedback_msg.remain_points))
            goal_handle.publish_feedback(feedback_msg)

            

        cnt = 0 #서빙할 메뉴 인덱스 count
        for j in goal[int(len(goal)/2):len(goal)]: #테이블 지점 (전체 인수의 절반)           
            self.send_point(self._dic_table[j][0], #테이블 딕셔너리에 저장된 좌표로 send_point 인수 대입
                            self._dic_table[j][1],
                            self._dic_table[j][2])
            while (str(goal[cnt]) != input()): #손님이 제대로 된 메뉴를 받아가는지 확인
                print(f"Wrong drink, Receive {self._dic_food[goal[cnt]]}")
            print(f"Received {self._dic_food[goal[cnt]]}") #메뉴 딕셔너리에 해당하는 메뉴 출력
            cnt += 1
            count_pnts += 1
            #order_action의 피드백 메시지 퍼블리시, 출력
            feedback_msg.remain_points = goal[count_pnts:int(len(goal))]
            self.get_logger().info('Feedback remain points: {0}'.format(feedback_msg.remain_points))
            goal_handle.publish_feedback(feedback_msg)
                
        #서빙 마친 후 원위치하여 다음 액션 호출 대기
        self.send_point(0.,0.,0.) 
        input()

        goal_handle.succeed()
        result.is_success = True
        return result
    
def main(args=None):
    rclpy.init(args=args)

    order_action_server = OrderActionServer()
    print("Action_server running...")

    rclpy.spin(order_action_server)

if __name__ == '__main__':
    main()    