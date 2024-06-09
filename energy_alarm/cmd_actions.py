from subprocess import run, PIPE, Popen

def ping(address, count = 1, ):
    result = run(f'ping -w 1 -c {count} {address}',shell= True,stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(result.returncode, result.stdout, result.stderr)
    return result.returncode == 0


def shut_down():
    cmdCommand = "shutdown -h now"
    return Popen(cmdCommand.split(), stdout=PIPE)
