# -- coding: utf-8 --
import os
import socket
import threading
import tensorflow as tf

'''
소켓 통신을 통해 파일을 전송 받아서 텐서플로우로 처리
'''
class ThreadServer(object):
    def __init__(self, host, port): # 클래스 생성 시 소켄 생성과 바인드 처리
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self): # 클라이언트를 기다림
        self.sock.listen(5)
        thread = threading.current_thread().name
        print(thread + ': 서버가 활성화 되었습니다 :)')
        while True:
            client, address = self.sock.accept()
            print(thread + ": 클라이언트가 연결됨 -> ", address)
            client.settimeout(30) # 30초 간 아무 동작이 없으면, 연결 해지
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        extension = (client.recv(4)).decode('utf-8') # 클라이언트로부터 확장자를 받아옴
        file_name = 'sample' + extension
        file_path = os.path.join('sample/', file_name).replace('\\', '.')
        thread = threading.current_thread().name
        with open(file_path, 'wb') as file: # 빈 파일을 생성하여, 다운로드 수행
            data = client.recv(1024)
            if not data:
                client.close()
            else:
                while data:
                    file.write(data)
                    if not data:
                        break
                    data = client.recv(1024)
                print(thread + ': 파일 전송 완료 -> ', address)
        if os.path.exists(file_path): # 파일이 정상적으로 다운로드 완료 되었으면,
            # 동영상인지 사진인지 체크
            if extension == '.jpg' or '.jpeg':
                # [핵심] 다운로드 받은 파일이 사진 인 경우 즉시, 텐서플로우를 통한 추론 개시
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
                label_lines = [line.rstrip() for line
                               in tf.gfile.GFile("retrained_labels.txt")]
                f = tf.gfile.FastGFile("retrained_graph.pb", 'rb')
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')
                image_path = file_path
                image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                with tf.Session() as sess:
                    result = []
                    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                    predictions = sess.run(softmax_tensor, \
                                           {'DecodeJpeg/contents:0': image_data})
                    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
                    for node_id in top_k:
                        human_string = label_lines[node_id]
                        score = predictions[0][node_id]
                        result.append('%s,%.5f' % (human_string, score)) # result 배열에 결과를 입력
                    print('[>] 인공신경망 추론결과 : ', result[0])
                    # 결과값을 클라이언트로 다시 알려줌
                    print('[>] 점검결과를 클라이언트로 회신합니다. / ', result[0])
                    client.send(result[0].encode('utf-8'))
                    print('[>] 클라이언트와 연결을 해지합니다.')
                    client.close() # 클라이언트와 연결 해지
            os.remove(file_path)

if __name__ == '__main__':
    # 서버의 네트워크 환경 정의
    TCP_IP = 'localhost'
    TCP_PORT = 9999

    # TCP 소켓 열고 수신 대기
    ThreadServer(TCP_IP, TCP_PORT).listen()

