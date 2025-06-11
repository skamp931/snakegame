import streamlit as st
import random
import time
import streamlit.components.v1 as components

# ゲーム設定
BOARD_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
GAME_SPEED = 0.2  # 秒

# HTML/JS for keyboard input
# This script listens for arrow key presses and sends the corresponding direction
# to Streamlit using `Streamlit.setComponentValue()`.
# It uses an invisible div to ensure the component exists but doesn't take up space.
keyboard_input_html = """
<script>
    const directionsMap = {
        'ArrowUp': 'up',
        'ArrowDown': 'down',
        'ArrowLeft': 'left',
        'ArrowRight': 'right'
    };

    document.addEventListener('keydown', function(event) {
        const newDirection = directionsMap[event.key];
        if (newDirection) {
            // Prevent default scroll behavior for arrow keys
            event.preventDefault();
            // Send the new direction value to Streamlit
            if (window.parent.Streamlit) {
                window.parent.Streamlit.setComponentValue(newDirection);
            }
        }
    });

    // Send an initial null value to ensure the component is rendered and ready.
    // This will trigger a rerun when the app first loads, but it's generally fine.
    if (window.parent.Streamlit) {
        window.parent.Streamlit.setComponentValue(null);
    }
</script>
<div style="width: 0; height: 0; overflow: hidden; position: absolute;"></div>
"""

st.set_page_config(layout="centered")

st.title("🐍 Streamlit スネークゲーム 🍎")

# Embed the keyboard input component.
# This will return the last value sent by `setComponentValue` from JS.
# If no key is pressed, it will be `None` (from the initial `setComponentValue(null)`).
last_key_input = components.html(keyboard_input_html, height=0, width=0, scrolling=False, key="keyboard_listener")

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

# キーボード入力に基づいて方向を更新
if last_key_input: # キーが実際に押された場合のみ更新（最初のnullではない）
    current_direction = st.session_state.direction # 現在の方向を取得

    # 方向ロジックを適用: 直前の逆方向には変更できない
    if last_key_input == 'up' and current_direction != 'down':
        st.session_state.direction = 'up'
    elif last_key_input == 'down' and current_direction != 'up':
        st.session_state.direction = 'down'
    elif last_key_input == 'left' and current_direction != 'right':
        st.session_state.direction = 'left'
    elif last_key_input == 'right' and current_direction != 'left':
        st.session_state.direction = 'right'

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
        new_head = (head_y - 1, head_x) # 修正: xとyが逆だったため修正
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

# スコアとゲームオーバーメッセージのプレースホルダー
score_placeholder = st.empty()
game_over_placeholder = st.empty()
board_placeholder = st.empty()

# ゲームオーバー時の表示
if st.session_state.game_over:
    game_over_placeholder.error(f"ゲームオーバー！あなたのスコア: {st.session_state.score}")
    if st.button("もう一度プレイ"):
        initialize_game_state()
        st.rerun() # ゲームをリスタートするために再実行

# 方向ボタンは削除されました

# ゲームループ
if not st.session_state.game_over:
    score_placeholder.write(f"スコア: {st.session_state.score}")

    # ヘビの移動 (st.session_state.direction はキーボード入力によって更新される)
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
