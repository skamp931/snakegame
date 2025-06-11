import streamlit as st
import random
import time

# ゲーム設定
BOARD_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
GAME_SPEED = 0.8  # 秒 (単語入力に合わせて遅くする)
INITIAL_WAIT_SECONDS = 5 # ゲーム開始前の待機時間

# 日本語とローマ字の単語リスト
japanese_words_romaji = {
    "こんにちは": "konnichiwa",
    "ありがとう": "arigatou",
    "さようなら": "sayounara",
    "おやすみ": "oyasumi",
    "おはよう": "ohayou",
    "はい": "hai",
    "いいえ": "iie",
    "ごめんなさい": "gomen nasai",
    "すみません": "sumimasen",
    "いただきます": "itadakimasu",
    "ごちそうさま": "gochisousama",
    "美味しい": "oishii",
    "楽しい": "tanoshii",
    "日本": "nihon",
    "東京": "toukyou",
    "寿司": "sushi",
    "ラーメン": "ramen",
    "桜": "sakura",
    "猫": "neko",
    "犬": "inu",
    "山": "yama",
    "川": "kawa",
    "海": "umi",
    "空": "sora",
    "星": "hoshi",
    "月": "tsuki",
    "太陽": "taiyou",
    "雨": "ame",
    "風": "kaze",
    "雪": "yuki",
    "花": "hana",
    "木": "ki",
    "水": "mizu",
    "火": "hi",
    "土": "tsuchi",
    "金": "kane",
    "銀": "gin",
    "銅": "dou",
    "鉄": "tetsu",
    "紙": "kami",
    "ペン": "pen",
    "本": "hon",
    "学校": "gakkou",
    "先生": "sensei",
    "生徒": "seito",
    "友達": "tomodachi",
    "家族": "kazoku",
    "父": "chichi",
    "母": "haha",
    "兄": "ani",
    "弟": "otouto",
    "姉": "ane",
    "妹": "imouto",
    "男": "otoko",
    "女": "onna",
    "子供": "kodomo",
    "大人": "otona",
    "時間": "jikan",
    "今日": "kyou",
    "明日": "ashita",
    "昨日": "kinou",
    "週": "shuu",
    "月": "tsuki",
    "年": "toshi",
    "朝": "asa",
    "昼": "hiru",
    "夜": "yoru",
    "数字": "suuji",
    "大きい": "ookii",
    "小さい": "chiisai",
    "高い": "takai",
    "低い": "hikui",
    "長い": "nagai",
    "短い": "mijikai",
    "速い": "hayai",
    "遅い": "osoi",
    "暑い": "atsui",
    "寒い": "samui",
    "熱い": "atsui",
    "冷たい": "tsumetai",
    "新しい": "atarashii",
    "古い": "furui",
    "良い": "yoi",
    "悪い": "warui",
    "可愛い": "kawaii",
    "美しい": "utsukushii",
    "面白い": "omoshiroi",
    "つまらない": "tsumaranai",
    "難しい": "muzukashii",
    "簡単": "kantan",
    "白い": "shiroi",
    "黒い": "kuroi",
    "赤い": "akai",
    "青い": "aoi",
    "黄色い": "kiiroi",
    "緑": "midori",
    "茶色": "chairo",
    "紫": "murasaki",
    "ピンク": "pinku",
    "オレンジ": "orenji",
    "灰色": "haiiro",
    "金色": "kin'iro",
    "銀色": "gin'iro",
    "透明": "toumei"
}

def get_random_word():
    """辞書からランダムな単語とそのローマ字を取得する"""
    japanese_word = random.choice(list(japanese_words_romaji.keys()))
    romaji_word = japanese_words_romaji[japanese_word]
    return japanese_word, romaji_word

# ゲームの状態をセッションステートに保存（初回ロード時またはリセット時）
# game_started が存在しない場合に全ての状態を初期化するように変更
if 'game_started' not in st.session_state:
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2 + i) for i in range(INITIAL_SNAKE_LENGTH)]
    st.session_state.food = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
    st.session_state.direction = 'left' # 初期方向をデフォルトで設定
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.word_input_key = 0 # テキスト入力のリセット用キー
    st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word() # 初期単語
    st.session_state.game_started = False # ゲームが開始されたかどうかのフラグ

def initialize_game_state():
    """ゲームの状態を初期化する関数"""
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2 + i) for i in range(INITIAL_SNAKE_LENGTH)]
    st.session_state.food = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
    st.session_state.direction = 'left' # 初期方向をデフォルトで設定
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.word_input_key += 1 # リセット時にキーを更新して入力フィールドをクリア
    st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word() # 新しい単語
    st.session_state.game_started = False # ゲームをリスタートする際もフラグをリセット

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

st.title("🐍 Streamlit ローマ字スネークゲーム 🍎")

# スコアとゲームオーバーメッセージのプレースホルダー
score_placeholder = st.empty()
game_over_placeholder = st.empty()
word_display_placeholder = st.empty() # 単語表示用
input_feedback_placeholder = st.empty() # 入力フィードバック用
board_placeholder = st.empty()
countdown_placeholder = st.empty() # カウントダウン表示用

# ゲームオーバー時の表示
if st.session_state.game_over:
    game_over_placeholder.error(f"ゲームオーバー！あなたのスコア: {st.session_state.score}")
    if st.button("もう一度プレイ"):
        initialize_game_state()
        st.rerun() # ゲームをリスタートするために再実行

# ゲーム開始前の5秒待機
# game_started のチェックを最初にすることで、未初期化エラーを防ぐ
if not st.session_state.game_started and not st.session_state.game_over:
    for i in range(INITIAL_WAIT_SECONDS, 0, -1):
        countdown_placeholder.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>ゲーム開始まで: {i}秒</h2>", unsafe_allow_html=True)
        time.sleep(1)
    countdown_placeholder.empty() # カウントダウン表示をクリア
    st.session_state.game_started = True
    st.rerun() # ゲーム本編を開始するために再実行

# メインゲームループ (ゲームが開始されており、かつゲームオーバーでない場合のみ実行)
if st.session_state.game_started and not st.session_state.game_over:
    score_placeholder.write(f"スコア: {st.session_state.score}")

    # ローマ字単語の表示
    word_display_placeholder.markdown(f"次の単語をローマ字で入力し、Enterキーを押して方向を変えてください: <br>**日本語:** {st.session_state.current_word_japanese} <br>**ローマ字:** `<span style='font-weight: bold; color: green;'>{st.session_state.current_word_romaji}</span>`", unsafe_allow_html=True)

    # テキスト入力フィールド
    user_input_romaji = st.text_input("ローマ字入力:", key=f"romaji_input_{st.session_state.word_input_key}")

    # ユーザー入力が正しいかチェック
    if user_input_romaji: # 入力があった場合のみ処理
        if user_input_romaji.lower() == st.session_state.current_word_romaji.lower():
            input_feedback_placeholder.success("正解！新しい方向を選択中...")

            current_direction = st.session_state.direction
            valid_directions = []

            # 進行方向と異なる方向、戻りはなしの方向に曲がる
            if current_direction in ['up', 'down']: # 現在が垂直方向の場合、左右に曲がる
                valid_directions = ['left', 'right']
            elif current_direction in ['left', 'right']: # 現在が水平方向の場合、上下に曲がる
                valid_directions = ['up', 'down']

            if valid_directions:
                new_direction = random.choice(valid_directions)
                st.session_state.direction = new_direction
            
            # 新しい単語を生成し、入力フィールドをリセット
            st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word()
            st.session_state.word_input_key += 1 # 入力フィールドをリセットするためにキーを更新
            st.rerun() # 方向が変わったことを即座に反映
            
        else:
            input_feedback_placeholder.warning("不正解です。もう一度試してください。")

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
        # 食べ物を食べたので新しい単語を生成し、入力フィードバックをクリア
        st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word()
        st.session_state.word_input_key += 1 # 入力フィールドをリセットするためにキーを更新
        input_feedback_placeholder.empty() # フィードバックをクリア


    # ゲームボードの表示を更新
    board_display_html = create_board_display(st.session_state.snake, st.session_state.food, BOARD_SIZE)
    board_placeholder.markdown(board_display_html, unsafe_allow_html=True)

    # 一定時間待機してから再実行 (ゲームの速度を制御)
    time.sleep(GAME_SPEED)
    st.rerun() # ページ全体を再実行して更新
