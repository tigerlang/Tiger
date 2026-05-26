// ============================================================
// ============================================================
#include <any>

namespace tiger_rt {

template<typename T, typename... Ts>
auto make_vec(T&& first, Ts&&... rest)
    -> std::vector<typename std::common_type<T, Ts...>::type>
{
    using CT = typename std::common_type<T, Ts...>::type;
    return std::vector<CT>{ static_cast<CT>(std::forward<T>(first)),
                            static_cast<CT>(std::forward<Ts>(rest))... };
}

template<typename T>
std::vector<T> make_vec() { return std::vector<T>{}; }

inline std::string str_upper(const std::string& s) {
    std::string r = s;
    std::transform(r.begin(), r.end(), r.begin(),
                   [](unsigned char c){ return (char)std::toupper(c); });
    return r;
}

inline std::string str_lower(const std::string& s) {
    std::string r = s;
    std::transform(r.begin(), r.end(), r.begin(),
                   [](unsigned char c){ return (char)std::tolower(c); });
    return r;
}

inline int str_len(const std::string& s) {
    return static_cast<int>(s.size());
}

inline std::string str_to_str(int v)    { return std::to_string(v); }
inline std::string str_to_str(long v)   { return std::to_string(v); }
inline std::string str_to_str(double v) { return std::to_string(v); }
inline int         str_to_int(const std::string& s)   { return std::stoi(s); }
inline double      str_to_float(const std::string& s) { return std::stod(s); }

inline std::string str_trim(const std::string& s) {
    size_t start = s.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    size_t end = s.find_last_not_of(" \t\n\r");
    return s.substr(start, end - start + 1);
}

inline std::vector<std::string> str_split(const std::string& s) {
    std::vector<std::string> res;
    std::istringstream iss(s);
    std::string w;
    while (iss >> w) res.push_back(w);
    return res;
}

inline bool str_startswith(const std::string& s, const std::string& prefix) {
    if (prefix.size() > s.size()) return false;
    return s.compare(0, prefix.size(), prefix) == 0;
}

inline bool str_endswith(const std::string& s, const std::string& suffix) {
    if (suffix.size() > s.size()) return false;
    return s.compare(s.size() - suffix.size(), suffix.size(), suffix) == 0;
}

} 
