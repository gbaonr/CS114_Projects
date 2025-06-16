import glob
import os
import argparse


def process_score(score):
    while len(score) < 3:
        score += "0"
    if len(score) > 3:
        score = score[:3]
    return int(float(int(score) / 10.0))


def get_score_and_id(folders):
    scores = []
    ids = []
    for folder in folders:
        preds = glob.glob(f"{folder}/*predict*.txt")
        pred2k = [f for f in preds if "2k" in f]
        pred10k = [f for f in preds if "10k" in f]
        pred2kname = os.path.basename(pred2k[0]) if pred2k else None
        pred10kname = os.path.basename(pred10k[0]) if pred10k else None

        try:
            score2k = process_score(pred2kname.replace(".txt", "").split("_")[-1])
            id2k = pred2kname.replace(".txt", "").split("_")[-2]
        except:
            score2k = "- "
            id2k = "  -   "

        try:
            score10k = process_score(pred10kname.replace(".txt", "").split("_")[-1])
            id10k = pred10kname.replace(".txt", "").split("_")[-2]
        except:
            score10k = " -"
            id10k = "  -   "

        folder_score = f"{score2k}/{score10k}"
        folder_id = f"{id2k} / {id10k}"

        scores.append(folder_score)
        ids.append(folder_id)
    return scores, ids


def print_table(title, folders, scores, ids):
    print("\n" * 2)
    print(f"## {title}")
    if not folders:
        print("Không có dữ liệu để hiển thị.")
        return

    index_col_width = max(len("STT"), len(str(len(folders))))
    folder_col_width = max(len("Model Version"), max(len(f) for f in folders))
    score_col_width = max(len("Scores (2k/10k)"), max(len(str(s)) for s in scores))
    id_col_width = max(len("Submit IDs (2k/10k)"), max(len(str(i)) for i in ids))

    # Header
    print(
        f"{'STT'.ljust(index_col_width)} | "
        f"{'Model Version'.ljust(folder_col_width)} | "
        f"{'Scores (2k/10k)'.ljust(score_col_width)} | "
        f"{'Submit IDs (2k/10k)'.ljust(id_col_width)}"
    )
    print(
        f"{'-' * index_col_width}-+-"
        f"{'-' * folder_col_width}-+-"
        f"{'-' * score_col_width}-+-"
        f"{'-' * id_col_width}"
    )

    # Rows
    for i, (folder, score, id_) in enumerate(zip(folders, scores, ids), start=1):
        print(
            f"{str(i).ljust(index_col_width)} | "
            f"{folder.ljust(folder_col_width)} | "
            f"{str(" "*5 + score).ljust(score_col_width)} | "
            f"{str(id_).ljust(id_col_width)}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create table with model info")
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="Number of top results to display (default: all).",
    )

    args = parser.parse_args()

    folder = os.getcwd()
    if os.path.basename(folder) != "hwd_checkpoints":
        folders = glob.glob("hwd_checkpoints/*/*")
        # print("Please run this script from the 'hwd_checkpoints' directory.")
        # exit(1)
    else:
        folders = glob.glob("*/*")
    folders = [f for f in folders if os.path.isdir(f)]
    folders = [f for f in folders if "no_submit" not in f]

    scores, ids = get_score_and_id(folders)

    # Ghép các phần tử thành list of tuples: (submit_id_for_sort, folder, score, id)
    combined = []
    for f, s, i in zip(folders, scores, ids):
        # Tách phần score 2k
        score_2k = s.split("/")[0].strip()
        score_10k = s.split("/")[1].strip()
        try:
            score_num = int(score_10k)
        except ValueError:
            score_num = 0
        try:
            score_num += int(score_2k)
        except ValueError:
            score_num += 0

        combined.append((score_num, f, s, i))

    # Sắp xếp theo score giảm dần
    combined_sorted = sorted(combined, key=lambda x: x[0], reverse=True)
    # combined_sorted = sorted(combined, key=lambda x: x[1].lower(), reverse=True) # sort by folder name

    # Tách ra 3 list mới
    folders = [c[1] for c in combined_sorted]
    scores = [c[2] for c in combined_sorted]
    ids = [c[3] for c in combined_sorted]

    # If top specified
    if args.top > 0:
        folders = folders[: args.top]
        scores = scores[: args.top]
        ids = ids[: args.top]

    print_table("Model Results", folders, scores, ids)
