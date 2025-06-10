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


def print_table(title, data_list):
    print("|\n" * 2)
    print(f"## {title}")
    if not data_list:
        print("Không có dữ liệu để hiển thị.")
        return

    max_res_len = max(len(res) for res, _ in data_list)
    score_col_width = 6

    print(f"{'Folder'.ljust(max_res_len)} | {'Score'.ljust(score_col_width)}")
    print(f"{'-' * max_res_len}-+-{'-' * score_col_width}")

    for res, score in data_list:
        print(f"{res.ljust(max_res_len)} | {str(score).ljust(score_col_width)}")
    print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create table")

    parser.add_argument(
        "--top",
        type=int,
        default=4,
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

    results2k = glob.glob("*/*/*predict_2k*.txt")
    results10k = glob.glob("*/*/*predict_10k*.txt")
    results2k = [r for r in results2k if "no_submit" not in r]
    results10k = [r for r in results10k if "no_submit" not in r]
    score2k = get_score(results2k)
    score10k = get_score(results10k)
    results2k_ = [os.path.dirname(r) for r in results2k]
    results10k_ = [os.path.dirname(r) for r in results10k]

    list10k = sorted(zip(results10k_, score10k), key=lambda x: x[1], reverse=True)
    list2k = sorted(zip(results2k_, score2k), key=lambda x: x[1], reverse=True)

    if args.set == "2k":
        print_table("Top 2k Results", list2k[: args.top])
    elif args.set == "10k":
        print_table("Top 10k Results", list10k[: args.top])
    else:
        print_table("Top 2k Results", list2k[: args.top])
        print_table("Top 10k Results", list10k[: args.top])
