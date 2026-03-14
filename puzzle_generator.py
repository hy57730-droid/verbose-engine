import random
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# -------------------------
# 6x6 ラテン方格のランダム生成
# -------------------------
def generate_random_solution():
    board = [[0] * 6 for _ in range(6)]

    def is_valid(r, c, n):
        if n in board[r]:
            return False
        for rr in range(6):
            if board[rr][c] == n:
                return False
        return True

    def dfs(cell=0):
        if cell == 36:
            return True
        r, c = divmod(cell, 6)

        nums = list(range(1, 7))
        random.shuffle(nums)

        for n in nums:
            if is_valid(r, c, n):
                board[r][c] = n
                if dfs(cell + 1):
                    return True
                board[r][c] = 0
        return False

    dfs()
    return board

# -------------------------
# 行ごとにヒントを残す（難易度調整）
# -------------------------
def make_balanced_puzzle(solution, hints_per_row):
    puzzle = [[0] * 6 for _ in range(6)]
    for r in range(6):
        cols = list(range(6))
        random.shuffle(cols)
        for c in cols[:hints_per_row]:
            puzzle[r][c] = solution[r][c]
    return puzzle

# -------------------------
# ランダムに追加で消す
# -------------------------
def remove_random_cells(puzzle, remove_count):
    cells = [(r, c) for r in range(6) for c in range(6) if puzzle[r][c] != 0]
    random.shuffle(cells)

    for i in range(min(remove_count, len(cells))):
        r, c = cells[i]
        puzzle[r][c] = 0

    return puzzle

# -------------------------
# 全解探索（2つ見つかったら打ち切り）
# -------------------------
def solve_all(board):
    solutions = [0]

    def is_valid(r, c, n):
        if n in board[r]:
            return False
        for rr in range(6):
            if board[rr][c] == n:
                return False
        return True

    def dfs():
        if solutions[0] >= 2:
            return

        for r in range(6):
            for c in range(6):
                if board[r][c] == 0:
                    for n in range(1, 7):
                        if is_valid(r, c, n):
                            board[r][c] = n
                            dfs()
                            board[r][c] = 0
                    return
        solutions[0] += 1

    dfs()
    return solutions[0]

# -------------------------
# 難易度別パズル生成
# -------------------------
def generate_puzzle(difficulty):
    if difficulty == "A":  # やさしい
        hints_per_row = 3
        extra_remove = 0
    elif difficulty == "B":  # ふつう
        hints_per_row = 2
        extra_remove = 2
    elif difficulty == "C":  # むずかしい
        hints_per_row = 2
        extra_remove = 4
    else:
        raise ValueError("難易度は A / B / C から選んでください")

    attempt = 1
    while True:
        print(f"試行 {attempt}: 完成盤を生成中…")
        solution = generate_random_solution()

        puzzle = make_balanced_puzzle(solution, hints_per_row)
        puzzle = remove_random_cells(puzzle, extra_remove)

        sol_count = solve_all([row[:] for row in puzzle])
        print(f"試行 {attempt}: 解の数 = {sol_count}")

        if sol_count == 1:
            print("一意解のパズルが完成しました。")
            return puzzle

        attempt += 1

# -------------------------
# PDF 出力（0 は空欄）＋ スクリプトと同じフォルダに保存
# -------------------------
def write_pdf(board, filename="puzzle6x6.pdf"):
    # スクリプトのあるフォルダに保存する
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    cell_size = 25 * mm
    start_x = (width - cell_size * 6) / 2
    start_y = height - 40 * mm

    c.setFont("Helvetica", 20)

    for r in range(6):
        for col in range(6):
            x = start_x + col * cell_size
            y = start_y - r * cell_size

            c.rect(x, y - cell_size, cell_size, cell_size)

            value = "" if board[r][col] == 0 else str(board[r][col])
            c.drawCentredString(x + cell_size / 2, y - cell_size / 2 - 5, value)

    c.showPage()
    c.save()
    print("PDF に書き出しました:", filepath)

# -------------------------
# メイン処理
# -------------------------
def main():
    difficulty = input("難易度を選んでください (A=やさしい / B=ふつう / C=むずかしい): ")
    puzzle = generate_puzzle(difficulty)
    write_pdf(puzzle)
    print("完了しました。")

if __name__ == "__main__":
    main()
