import streamlit as st
import random
import time

# ゲーム設定
BOARD_SIZE = 12
INITIAL_SNAKE_LENGTH = 3
INITIAL_WAIT_SECONDS = 5 # ゲーム開始前の待機時間

# 難易度ごとのゲーム速度設定 (秒)
DIFFICULTY_SPEEDS = {
    "簡単": 2.0,   # Slowest
    "普通": 1.5,   # Normal (default previously)
    "難しい": 1.0, # Faster
    "鬼ムズ": 0.3  # Fastest
}

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
    "金色": "kiniro",
    "銀色": "giniro",
    "透明": "toumei"
}

def get_random_word():
    """辞書からランダムな単語とそのローマ字を取得する"""
    japanese_word = random.choice(list(japanese_words_romaji.keys()))
    romaji_word = japanese_words_romaji[japanese_word]
    return japanese_word, romaji_word

# ゲームの状態をセッションステートに保存（初回ロード時またはリセット時）
# すべてのセッションステート変数をここで初期化することで、AttributeErrorを防ぐ
# difficultyとgame_speedはselect_boxより前に確実に初期化されるようにする
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "普通" # デフォルトの難易度設定
if 'game_speed' not in st.session_state:
    st.session_state.game_speed = DIFFICULTY_SPEEDS[st.session_state.difficulty] # 難易度に応じたゲーム速度

if 'game_started' not in st.session_state:
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2 + i) for i in range(INITIAL_SNAKE_LENGTH)]
    # 果物の配置をボードの内側（外周1マスを避ける）に制限
    st.session_state.food = (random.randint(1, BOARD_SIZE - 2), random.randint(1, BOARD_SIZE - 2))
    st.session_state.direction = 'left' # 初期方向をデフォルトで設定
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.word_input_key = 0 # テキスト入力のリセット用キー
    st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word() # 初期単語
    st.session_state.game_started = False # ゲームが開始されたかどうかのフラグ
    st.session_state.initial_countdown_done = False # 初回カウントダウンが完了したかどうかのフラグ


def initialize_game_state():
    """ゲームの状態を初期化する関数"""
    st.session_state.snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2 + i) for i in range(INITIAL_SNAKE_LENGTH)]
    # 果物の配置をボードの内側（外周1マスを避ける）に制限
    st.session_state.food = (random.randint(1, BOARD_SIZE - 2), random.randint(1, BOARD_SIZE - 2))
    st.session_state.direction = 'left' # 初期方向をデフォルトで設定
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.word_input_key += 1 # リセット時にキーを更新して入力フィールドをクリア
    st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word() # 新しい単語
    st.session_state.game_started = False # ゲームをリスタートする際もフラグをリセット
    st.session_state.initial_countdown_done = False # カウントダウンもリセット
    # 難易度とゲーム速度はリセット時に保持
    st.session_state.game_speed = DIFFICULTY_SPEEDS[st.session_state.difficulty]

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
input_box_placeholder = st.empty() # 入力ボックス用
tab_key_hint_placeholder = st.empty() # Tabキーヒント用
board_placeholder = st.empty()
countdown_placeholder = st.empty() # カウントダウン表示用

# 難易度設定
# difficultyが確実に初期化された後にアクセスするように修正
selected_difficulty = st.selectbox(
    "難易度を選択してください:",
    options=list(DIFFICULTY_SPEEDS.keys()),
    index=list(DIFFICULTY_SPEEDS.keys()).index(st.session_state.difficulty),
    key="difficulty_selector"
)
# 難易度が変更されたらセッションステートとゲーム速度を更新
if selected_difficulty != st.session_state.difficulty:
    st.session_state.difficulty = selected_difficulty
    st.session_state.game_speed = DIFFICULTY_SPEEDS[selected_difficulty]
    # 難易度変更時にゲームを初期化するかどうかは要検討 (ここでは初期化しない)
    # st.rerun() # 必要に応じて難易度変更時にページを再実行

# ゲームオーバー時の表示
if st.session_state.game_over:
    game_over_placeholder.error(f"ゲームオーバー！あなたのスコア: {st.session_state.score}")
    if st.button("もう一度プレイ"):
        initialize_game_state()
        st.rerun() # ゲームをリスタートするために再実行

# --- 常に表示されるUI要素 (ゲームオーバー時以外) ---
if not st.session_state.game_over:
    score_placeholder.write(f"スコア: {st.session_state.score}")

    # ローマ字単語の表示
    word_display_placeholder.markdown(
        f"次の単語をローマ字で入力し、Enterキーを押して方向を変えてください: <br>"
        f"**日本語:** {st.session_state.current_word_japanese} <br>"
        f"**ローマ字:** <span style='font-weight: bold; color: green; font-size: 1.2em;'>{st.session_state.current_word_romaji}</span>",
        unsafe_allow_html=True
    )

    # テキスト入力フィールド (ローマ字の下に表示)
    with input_box_placeholder:
        # disabled属性を削除し、ゲーム開始前でも入力できるようにする
        user_input_romaji = st.text_input(
            "ローマ字入力:",
            key=f"romaji_input_{st.session_state.word_input_key}",
            label_visibility="collapsed"
        )
    
    # Tabキーヒントの表示
    tab_key_hint_placeholder.info("ヒント：Tabキーで入力ボックスを選択できます。")

    # ゲームボードの初期表示 (常に表示)
    board_display_html = create_board_display(st.session_state.snake, st.session_state.food, BOARD_SIZE)
    board_placeholder.markdown(board_display_html, unsafe_allow_html=True)


# --- ゲーム開始前の5秒待機 ---
if not st.session_state.game_started and not st.session_state.game_over and not st.session_state.initial_countdown_done:
    # ローマ字入力ボックスとボードが表示されてからカウントダウンを開始
    for i in range(INITIAL_WAIT_SECONDS, 0, -1):
        countdown_placeholder.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>ゲーム開始まで: {i}秒</h2>", unsafe_allow_html=True)
        time.sleep(1)
    countdown_placeholder.empty() # カウントダウン表示をクリア
    st.session_state.game_started = True
    st.session_state.initial_countdown_done = True # カウントダウンが完了したことをマーク
    st.rerun() # ゲーム本編を開始するために再実行


# メインゲームループ (ゲームが開始されており、かつゲームオーバーでない場合のみ実行)
if st.session_state.game_started and not st.session_state.game_over:
    # ユーザー入力が正しいかチェック
    if user_input_romaji: # 入力があった場合のみ処理
        if user_input_romaji.lower() == st.session_state.current_word_romaji.lower():
            input_feedback_placeholder.success("正解！新しい方向を選択中...")

            current_direction = st.session_state.direction
            
            # 曲がる方向を決定するロジック（ぶつかるまでの距離が長い方）
            distances = {}
            head_x, head_y = st.session_state.snake[0]

            if current_direction in ['up', 'down']: # 現在が垂直方向の場合、左右に曲がる
                # 左への距離
                distances['left'] = head_y
                # 右への距離
                distances['right'] = BOARD_SIZE - 1 - head_y
            elif current_direction in ['left', 'right']: # 現在が水平方向の場合、上下に曲がる
                # 上への距離
                distances['up'] = head_x
                # 下への距離
                distances['down'] = BOARD_SIZE - 1 - head_x

            new_direction = None
            if distances:
                max_distance = -1
                best_directions = []
                for direction, dist in distances.items():
                    if dist > max_distance:
                        max_distance = dist
                        best_directions = [direction]
                    elif dist == max_distance:
                        best_directions.append(direction)
                
                # 最長距離の方向が複数ある場合はランダムに選択
                new_direction = random.choice(best_directions)
                st.session_state.direction = new_direction
            
            # 新しい単語を生成し、入力フィールドをリセット
            st.session_state.current_word_japanese, st.session_state.current_word_romaji = get_random_word()
            st.session_state.word_input_key += 1 # 入力フィールドをリセットするためにキーを更新
            st.rerun() # 方向が変わったことを即座に反映
            
        else:
            input_feedback_placeholder.warning("不正解です。もう一度試してください。")
            # 不正解の場合、入力ボックスをクリアしない（ユーザーが修正できるように）

    # ヘビの移動
    st.session_state.snake, eats_food = move_snake(st.session_state.snake, st.session_state.direction, st.session_state.food, BOARD_SIZE)

    if eats_food:
        st.session_state.score += 1
        # 新しい食べ物を生成 (ヘビの体と重ならないように)
        # 果物の配置をボードの内側（外周1マスを避ける）に制限
        while True:
            new_food = (random.randint(1, BOARD_SIZE - 2), random.randint(1, BOARD_SIZE - 2))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
        # 食べ物を食べた際に単語を変更しない (ユーザーの要望による変更)

    # ゲームボードの表示を更新 (ループ内で継続的に更新)
    board_display_html = create_board_display(st.session_state.snake, st.session_state.food, BOARD_SIZE)
    board_placeholder.markdown(board_display_html, unsafe_allow_html=True)

    # 一定時間待機してから再実行 (ゲームの速度を制御)
    time.sleep(st.session_state.game_speed) # 難易度に応じた速度を使用
    st.rerun() # ページ全体を再実行して更新
