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
# 一意性を保ちながら削除する方式（難易度調整）
# -------------------------
def generate_puzzle(difficulty):
    solution = generate_random_solution()
    puzzle = [row[:] for row in solution]

    # ★ 新しい難易度設定（ヒント総数）
    if difficulty == "A":      # 最も易しい
        target_clues = 20
    elif difficulty == "B":    # 中間
        target_clues = 18
    elif difficulty == "C":    # 最も難しい
        target_clues = 16
    else:
        raise ValueError("難易度は A / B / C から選んでください")

    # 全セルをシャッフルして削除候補順を作る
    cells = [(r, c) for r in range(6) for c in range(6)]
    random.shuffle(cells)

    for r, c in cells:
        current_clues = sum(1 for rr in range(6) for cc in range(6) if puzzle[rr][cc] != 0)
        if current_clues <= target_clues:
            break

        backup = puzzle[r][c]
        puzzle[r][c] = 0

        sol_count = solve_all([row[:] for row in puzzle])
        if sol_count != 1:
            puzzle[r][c] = backup  # 一意でなくなったら戻す

    return puzzle

# -------------------------
# PDF 出力（0 は空欄）
# -------------------------
def write_pdf(board, filename="puzzle6x6.pdf"):
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
