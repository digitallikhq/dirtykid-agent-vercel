from dirtykid_agent import run_dirty_kid


def main():
    result = run_dirty_kid()
    print("Dirty Kid run complete.")
    print(result["post"])


if __name__ == "__main__":
    main()
