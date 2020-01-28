#include <iostream>
#include <string>
#include <vector>
#include <assert.h>

static const int32_t MAX_VOCAB_SIZE = 30000000;
static const int32_t BUCKET_SIZE = 2000000;
static const int32_t MIN_NGRAM_SIZE = 3;
static const int32_t MAX_NGRAM_SIZE = 6;
static std::string PREFIX_LABEL = "_label_";
static const std::string EOS = "</s>";
static const std::string BOW = "<";
static const std::string EOW = ">";

enum class entry_type : int8_t {word=0, label=1};
struct entry {
    std::string word;
    int64_t count;
    entry_type type;
    std::vector<int32_t> subwords;
};

std::vector<entry> words_;
int32_t size_ = 0;
int32_t nwords_ = 0;
int32_t nlabels_ = 0;
int32_t ntokens_ = 0;
std::vector<int32_t> word2int_;

static void init() {
  size_ = 0;
  nwords_ = 0;
  nlabels_ = 0;
  ntokens_ = 0;
  word2int_.resize(MAX_VOCAB_SIZE);
  for (int32_t i = 0; i < MAX_VOCAB_SIZE; i++) {
    word2int_[i] = -1;
  }
}

static uint32_t hash(const std::string& str) {
    uint32_t h = 2166136261;
    for (size_t i = 0; i < str.size(); i++) {
        h = h ^ uint32_t(str[i]);
        h = h * 16777619;
    }
    return h;
}

static int32_t find(const std::string& w) {
    int32_t h = hash(w) % MAX_VOCAB_SIZE;
    while (word2int_[h] != -1 && words_[word2int_[h]].word != w) {
        h = (h + 1) % MAX_VOCAB_SIZE;
    }
    return h;
}

static void add(const std::string& w) {
    int32_t h = find(w);
    ntokens_++;
    if (word2int_[h] == -1) {
        entry e;
        e.word = w;
        e.count = 1;
        e.type = (w.find(PREFIX_LABEL) == 0) ? entry_type::label : entry_type::word;
        if (e.type == entry_type::word) nwords_++;
        if (e.type == entry_type::label) nlabels_++;
        words_.push_back(e);
        word2int_[h] = size_++;
    } else {
        words_[word2int_[h]].count++;
    }
}

static int32_t getId(const std::string& w) {
    int32_t h = find(w);
    return word2int_[h];
}

static entry_type getType(int32_t id) {
    assert(id >= 0);
    assert(id < size_);
    return words_[id].type;
}

static std::string getWord(int32_t id) {
    assert(id >= 0);
    assert(id < size_);
    return words_[id].word;
}

static void computeNgrams(const std::string& word,
                    std::vector<int32_t>& ngrams) {
    for (size_t i = 0; i < word.size(); i++) {
        std::string ngram;
        if ((word[i] & 0xC0) == 0x80) continue;
        for (size_t j = i, n = 1; j < word.size() && n <= MAX_NGRAM_SIZE; n++) {
            ngram.push_back(word[j++]);
            while (j < word.size() && (word[j] & 0xC0) == 0x80) {
                ngram.push_back(word[j++]);
            }
            if (n >= MIN_NGRAM_SIZE && !(n == 1 && (i == 0 || j == word.size()))) {
                int32_t h = hash(ngram) % BUCKET_SIZE;
                std::cout << ngram << "\t" << h << std::endl;
                ngrams.push_back(nwords_ + h);
            }
        }
    }
}

static void initNgrams() {
    for (size_t i = 0; i < size_; i++) {
        std::string word = BOW + words_[i].word + EOW;
        words_[i].subwords.push_back(i);
        computeNgrams(word, words_[i].subwords);
    }
}

static const std::vector<int32_t>& getNgrams(int32_t i) {
    assert(i >= 0);
    assert(i < nwords_);
    return words_[i].subwords;
}

static const std::vector<int32_t> getNgrams(const std::string& word) {
    int32_t i = getId(word);
    if (i >= 0) {
        return getNgrams(i);
    }
    std::vector<int32_t> ngrams;
    computeNgrams(BOW + word + EOW, ngrams);
    return ngrams;
}

int main(int argc, char** argv) {

    init();

    std::string word1 = "카카오12검색";
    std::string word2 = "ab네이버구글34";

    add(word1);
    add(word2);

    initNgrams();

    return 0;
}
