import argparse

from common.slave_node import SlaveNode


def main():

    parser = argparse.ArgumentParser(description="启动slave节点")
    parser.add_argument("command", help="要执行的命令（例如 runclient）")
    args = parser.parse_args()
    slave_client = SlaveNode()
    if args.command == "runclient":
        slave_client.check()
    elif args.command == "getkey":
        slave_client.get_key()
    else:
        print(f"未知命令: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()