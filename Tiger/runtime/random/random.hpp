// ============================================================
// ============================================================
#include <random>

namespace tiger_random {

static std::mt19937& _gen() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    return gen;
}

int int_range(int min, int max) {
    std::uniform_int_distribution<int> dist(min, max);
    return dist(_gen());
}

double float_range(double min, double max) {
    std::uniform_real_distribution<double> dist(min, max);
    return dist(_gen());
}

int randint(int max) {
    return int_range(0, max - 1);
}

double random() {
    return float_range(0.0, 1.0);
}

void seed(int s) {
    _gen().seed(s);
}

} 