# 職務経歴書

## 個人データ
- 氏名: 藤野 暢 (Toru Fujino)
- GitHub: https://github.com/toru34
- Slideshare: https://www.slideshare.net/torufujino
- LinkedIn: https://www.linkedin.com/in/toru34

## プログラミングスキル
- Python
    - 2015年から現在まで, ML/NLP/DL等の用途で使用.
    - 使用ライブラリ: NumPy, Matplotlib, Tensorflow(v1), PyTorch等.
    - 参考となるレポジトリ
        - VAEを用いたテキスト生成モデル (EMNLP2019で発表された論文の再現実装. 開発途中): https://github.com/toru34/li_emnlp_2019
        - GANを用いたテキスト生成モデル (NeurIPS2019で発表された論文の再現実装. 開発途中): https://github.com/toru34/dautume_neurips_2019
        - VAE+Encoder-Decoderを用いた文書要約モデル (EMNLP2017で発表された論文の再現実装): https://github.com/toru34/li_emnlp_2017
- C++:
    - 2014年から現在まで, 修士/博士での研究 (Agent-basedモデルの構築) 等で使用.
    - 使用ライブラリ: 基本的なSTL.
    - 参考となるレポジトリ
        - Q学習を用いた少数派ゲームのモデル化 (Physical Review Eで発表された論文の再現実装): (https://github.com/toru34/Andrecut_PRE_2001)
        - 少数派ゲームを用いた経路選択モデル (自身で執筆した論文の公開実装): (https://github.com/toru34/fujino_physica_2019)
- SQL
    - 基本的な文法のみ. 必要になったときに毎回調べながら.

## これからやってみたいこと
- 自然言語処理/機械学習の研究開発.
    - 既存のモデルを当てはめるだけに終わらない高度なドメイン知識が要求される領域.
    - 自然言語生成 (例えば新聞記事の自動生成, 契約文書の自動生成など).

## 職務経歴

### 特任研究員 (非常勤) at 国立研究開発法人 国立がん研究センター東病院 (2020.01 ~ 現在)

#### 1. 深層学習技術を用いた医用画像解析 (2020.01 ~ 現在)

- 大腸がん手術を部分的に自動化するシステムの要素技術の開発に従事.
- 外科医・アノテータ・プロジェクトマネージャ等との連携の下, 開発の方向性を適宜確認・修正しながらプロジェクトを遂行.
- 取り組んでいるタスク: セマンティックセグメンテーション・物体検出等.
- 使用している技術: Python (Keras, PyTorch, OpenCV, NumPy).

### データサイエンティスト (契約社員) at 株式会社IGPIビジネスアナリティクス&インテリジェンス (2015.12 ~ 2018.04, 2018.10 ~ 2019.11)

#### 1. 教育機関における深層学習講座の教材作成 (2016.04 ~ 2019.11)

- 学生TAの一人として深層学習の基礎技術 (MLP, CNN, RNN, etc.) 及び応用技術 (CV, NLP, RL, etc.) についての教材作成に従事.
- 専門外のトピックの教材作成に携わる際は, その都度教科書・論文の読み込み等を自主的に行うことで技術を習得.
- 使用した技術: Python (NumPy, Theano, TensorFlow(v1)/Keras, PyTorch)
- 関わった講座
    - DL4US (2018年 ~ 2019年) \[[Link](https://weblab.t.u-tokyo.ac.jp/dl4us/)\]
        - 深層学習を広く浅く学ぶ社会人 (エンジニア) 向けのオンライン講座 (全7回).
        - Kerasの高レベルなAPIを用いた実装が中心.
        - CNNを用いた画像分類, CNN+RNNを用いた画像のキャプション生成, DQNによる強化学習の回の教材作成を担当.
        - 参考となるレポジトリ: https://github.com/matsuolab-edu/dl4us
    - 深層学習 (2016年 ~ 2019年) \[[Link](https://deeplearning.jp/lectures/dlb2018/)]
        - 深層学習全般を扱う大学生/大学院生向けの講座 (全11回) .
        - NumPy, TensorFlowの低レベルなAPIを用いた実装が中心.
        - NumPyによるkNNの実装, NumPyによるMLP/RNNの実装, TensorFlow入門, RNNを用いた機械翻訳, CNN+RNNを用いた画像のキャプション生成の回を主に担当.
    - Deep Learning for NLP サマースクール (2018年) \[[Link](https://deeplearning.jp/deep-learning-for-nlp/)]
        - 大学院生向けの短期講座 (全6回) .
        - PyTorch入門, 生成モデル (VAE, GAN) を用いたテキスト生成の回の教材作成を主に担当.

#### 2. 新聞記事の自動生成アルゴリズムの開発 (日経新聞社との共同研究, 2015.12 ~ 2018.01頃)

- 日経新聞社の記者・エンジニアとの連携の下, 学生メンバーの一人として企業が発行する決算短信から速報記事を自動で生成するアルゴリズムの開発に従事.
- 新聞記事では内容の正確さ・生成記事の文法的な正しさが高いレベルで求められるため, 深層学習や機械学習だけでなく正確性の高いルールベース (テンプレートの利用など) のアルゴリズムを組み合わせて使用.
- 使用した技術: Python (Theano, TensorFlow, MeCab, etc.), MySQL.
- XBRL (XMLに似たデータ構造) からの数値データの抽出, ルールベース/深層学習を用いた文生成アルゴリズムの開発/実装, 学生リーダーとしてのプロジェクト全体のマネジメントを主に担当.
- 宣伝サイト: https://pr.nikkei.com/qreports-ai/

## その他のスキル
- 英語
    - 所属する研究室での定例MTGでの発表, 留学生のチューター, 国際会議での発表, 雑誌論文の執筆等.
    - TOEFL iBT: 96点 (2016年9月取得).
- LaTeX
    - 論文を書く際に使用.
- GitHub
    - コード執筆を伴う開発を行う際に日常的に使用.

## 補足
- この職務経歴書の作成に際して「エンジニアが読みたくなる職務経歴書」https://dwango.github.io/articles/engineers-resume/ を参考にさせていただきました.
