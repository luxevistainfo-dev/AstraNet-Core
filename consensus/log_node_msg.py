# consensus/log_node_msg.py

def log_node_msg(sender, receiver, message):
    """
    Логирај сè што node-ите праќаат помеѓу себе.
    """
    with open("node_comm.log", "a") as f:
        f.write(f"{sender}->{receiver}: {message}\n")

