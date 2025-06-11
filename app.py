import streamlit as st
import random
import time

# ゲーム設定
BOARD_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
GAME_SPEED = 0.2  # 秒

# ゲームの状態をセッションステートに保存（初回ロード時またはリセット時）
if 'snake' not in st.session_state:
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2 + i) for i in range(INITIAL_SNAKE_LENGTH)]
    st.session_state.food = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
    st.session_state.direction = 'left' # 初期方向をデフォルトで設定
    st.session_state.score = 0
    st.session_state.game_over = False

def initialize_game_state():
    """ゲームの状態を初期化する関数"""
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2 + i) for i in range(INITIAL_SNAKE_LENGTH)]
    st.session_state.food = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
    st.session_state.direction = 'left' # 初期方向をデフォルトで設定
    st.session_state.score = 0
    st.session_state.game_over = False

def create_board_display(snake, food, board_size):
    """ゲームボードを文字列で表現して表示する"""
    board = [["⬜" for _ in range(board_size)] for _ in range(board_size)]

    # ヘビの頭を表示
    head_x, head_y = snake[0]
    board[head_x][head_y] = "🐍"

    # ヘビの体を表示
    for segment_x, segment_y in snake[1:]:
        board[segment_x][segment_y] = "🟩"

    # 食べ物を表示
    food_x, food_y = food
    board[food_x][food_y] = "🍎"

    # ボードを整形して表示
    board_str = "<div style='font-family: monospace; font-size: 24px; line-height: 1;'>"
    for row in board:
        board_str += "".join(row) + "<br>"
    board_str += "</div>"
    return board_str


def move_snake(snake, direction, food, board_size):
    """ヘビを動かし、衝突を検出する"""
    head_x, head_y = snake[0]
    new_head = (head_x, head_y)

    if direction == 'up':
        new_head = (head_x - 1, head_y)
    elif direction == 'down':
        new_head = (head_x + 1, head_y)
    elif direction == 'left':
        new_head = (head_x, head_y - 1)
    elif direction == 'right':
        new_head = (head_x, head_y + 1)

    # 壁との衝突判定
    if not (0 <= new_head[0] < board_size and 0 <= new_head[1] < board_size):
        st.session_state.game_over = True
        return snake, False # 衝突でゲームオーバー

    # 自分自身との衝突判定 (新しい頭が既存の体にぶつかるか)
    if new_head in snake:
        st.session_state.game_over = True
        return snake, False # 衝突でゲームオーバー

    new_snake = [new_head] + snake[:]
    eats_food = (new_head == food)

    if not eats_food:
        new_snake.pop() # 食べなければ尻尾を削除

    return new_snake, eats_food

st.set_page_config(layout="centered")

st.title("🐍 Streamlit スネークゲーム 🍎")

# スコアとゲームオーバーメッセージのプレースホルダー
score_placeholder = st.empty()
game_over_placeholder = st.empty()
board_placeholder = st.empty()

# キーボードコマンド用のテキスト入力フィールド
# ユーザーは 'w', 'a', 's', 'd' を入力し、Enterキーを押す必要があります。
st.write("キーボードで方向を入力してください (w:上, s:下, a:左, d:右) そしてEnterを押してください。")
direction_input = st.text_input("次の移動方向:", max_chars=1, key="direction_input")

# ゲームオーバー時の表示
if st.session_state.game_over:
    game_over_placeholder.error(f"ゲームオーバー！あなたのスコア: {st.session_state.score}")
    if st.button("もう一度プレイ"):
        initialize_game_state()
        st.rerun() # ゲームをリスタートするために再実行

# 方向の更新ロジック (テキスト入力から)
# 新しい方向が入力され、それが有効なキーである場合のみ更新
if direction_input:
    current_direction = st.session_state.direction
    new_input_direction = direction_input.lower()

    if new_input_direction == 'w' and current_direction != 'down':
        st.session_state.direction = 'up'
    elif new_input_direction == 's' and current_direction != 'up':
        st.session_state.direction = 'down'
    elif new_input_direction == 'a' and current_direction != 'right':
        st.session_state.direction = 'left'
    elif new_input_direction == 'd' and current_direction != 'left':
        st.session_state.direction = 'right'

# ゲームループ
if not st.session_state.game_over:
    score_placeholder.write(f"スコア: {st.session_state.score}")

    # ヘビの移動
    st.session_state.snake, eats_food = move_snake(st.session_state.snake, st.session_state.direction, st.session_state.food, BOARD_SIZE)

    if eats_food:
        st.session_state.score += 1
        # 新しい食べ物を生成 (ヘビの体と重ならないように)
        while True:
            new_food = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    
    # ゲームボードの表示を更新
    board_display_html = create_board_display(st.session_state.snake, st.session_state.food, BOARD_SIZE)
    board_placeholder.markdown(board_display_html, unsafe_allow_html=True)

    # 一定時間待機してから再実行 (ゲームの速度を制御)
    time.sleep(GAME_SPEED)
    st.rerun() # ページ全体を再実行して更新
