import base64
import uuid
import zmq

def test_zmq_embdserver(image_file_name):
    _rid = "{}".format(str(uuid.uuid4()))

    global img_str

    with open(image_file_name, "rb") as image_file:
        img_str = base64.b64encode(image_file.read())

    print(type(img_str))
    img_str = img_str.decode('ascii') 
    
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.setsockopt_string(zmq.IDENTITY, _rid)
    socket.connect('tcp://localhost:62058')
    print('Client %s started\n' % _rid)
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    obj = socket.send_json({"payload": img_str, "_rid": _rid})
    print('object snet')
    received_reply = False
    while not received_reply:
        sockets = dict(poll.poll(1000))
        if socket in sockets:
            if sockets[socket] == zmq.POLLIN:
                msg = socket.recv_json()
                preds = msg['preds']
                print(preds)
                del msg
                received_reply = True

    socket.close()
    context.term()

if __name__ == "__main__":
    name = './hindi.jpeg'
    test_zmq_embdserver(name)
