import glob
import os
import argparse


def get_score(results):
    scores = []
    for res in results:
        basename = os.path.basename(res).replace(".txt", "")
        score = basename.split("_")[-1]
        while len(score) < 3:
            score += "0"
        if len(score) > 3:
            score = score[:3]
        scores.append(int(float(score) / 10.0))
    return scores


def remove_ungraded(results):
    finals = []
    for res in results:
        files = os.listdir(os.path.dirname(res))
        if "predict_2k.txt" not in files or "predict_10k.txt" not in files:
            finals.append(res)
    return finals


def print_table(title, data_list):
    print("|\n" * 2)
    print(f"## {title}")
    if not data_list:
        print("Không có dữ liệu để hiển thị.")
        return

    index_col_width = max(len(str(len(data_list))), len("Index"))

    max_res_len = max(len(res) for res, _ in data_list)
    score_col_width = 6

    print(
        f"{'Index'.ljust(index_col_width)} | {'Folder'.ljust(max_res_len)} | {'Score'.ljust(score_col_width)}"
    )
    print(f"{'-' * index_col_width}-+-{'-' * max_res_len}-+-{'-' * score_col_width}")

    for i, (res, score) in enumerate(data_list):
        print(
            f"{str(i+1).ljust(index_col_width)} | {res.ljust(max_res_len)} | {str(score).ljust(score_col_width)}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create table")

    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="Number of top results to display (default: all).",
    )
    parser.add_argument(
        "--set",
        type=str,
        default="all",
        choices=["2k", "10k", "all"],
        help='Specify the dataset to analyze: "2k", "10k", or "all" (default: "all").',
    )

    args = parser.parse_args()

    results2k = glob.glob("*/*/*predict*2k*.txt")
    results10k = glob.glob("*/*/*predict*10k*.txt")

    results2k = [r for r in results2k if "no_submit" not in r]
    results10k = [r for r in results10k if "no_submit" not in r]
    results2k = remove_ungraded(results2k)
    results10k = remove_ungraded(results10k)
    score2k = get_score(results2k)
    score10k = get_score(results10k)
    results2k_ = [os.path.dirname(r) for r in results2k]
    results10k_ = [os.path.dirname(r) for r in results10k]

    list10k = sorted(zip(results10k_, score10k), key=lambda x: x[1], reverse=True)
    list2k = sorted(zip(results2k_, score2k), key=lambda x: x[1], reverse=True)

    if args.top > len(list2k) or args.top > len(list10k):
        args.top = min(len(list2k), len(list10k))

    if args.top <= 0:
        args.top = max(len(list2k), len(list10k)) + 2

    # print("".ljust(70, "-"))
    if args.set == "2k":
        print_table("Top 2k Results", list2k[: args.top])
    elif args.set == "10k":
        print_table("Top 10k Results", list10k[: args.top])
    else:
        print_table("Top 2k Results", list2k[: args.top])
        print_table("Top 10k Results", list10k[: args.top])

    print("".ljust(70, "-"))
