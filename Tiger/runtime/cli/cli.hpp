// ============================================================
// ============================================================
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>

namespace tiger_cli {

static std::map<std::string, std::string> _args;
static bool _args_parsed = false;

namespace colors {
    const std::string reset   = "\033[0m";
    const std::string red     = "\033[91m";
    const std::string yellow  = "\033[93m";
    const std::string green   = "\033[92m";
    const std::string blue    = "\033[94m";
    const std::string gray    = "\033[90m";
}

void parse_args(int argc, char* argv[]) {
    if (_args_parsed) return;
    _args_parsed = true;
    
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg.substr(0, 2) == "--") {
            size_t eq = arg.find('=', 2);
            if (eq != std::string::npos) {
                std::string key = arg.substr(2, eq - 2);
                std::string val = arg.substr(eq + 1);
                _args[key] = val;
            } else {
                std::string key = arg.substr(2);
                if (i + 1 < argc && argv[i + 1][0] != '-') {
                    _args[key] = argv[++i];
                } else {
                    _args[key] = "true";
                }
            }
        } else if (arg[0] == '-' && arg.size() > 1) {
            char key = arg[1];
            std::string key_str(1, key);
            if (i + 1 < argc && argv[i + 1][0] != '-') {
                _args[key_str] = argv[++i];
            } else {
                _args[key_str] = "true";
            }
        }
    }
}

std::string get(const std::string& key, const std::string& def) {
    auto it = _args.find(key);
    return it != _args.end() ? it->second : def;
}

int get_int(const std::string& key, int def) {
    auto it = _args.find(key);
    if (it == _args.end()) return def;
    int val;
    std::istringstream(it->second) >> val;
    return val;
}

bool has(const std::string& key) {
    return _args.find(key) != _args.end();
}

bool is_help() {
    return has("help") || has("h");
}

void error(const std::string& msg) {
    std::cerr << colors::red << msg << colors::reset << std::endl;
}

void warning(const std::string& msg) {
    std::cout << colors::yellow << msg << colors::reset << std::endl;
}

void success(const std::string& msg) {
    std::cout << colors::green << msg << colors::reset << std::endl;
}

void info(const std::string& msg) {
    std::cout << colors::blue << msg << colors::reset << std::endl;
}

void debug(const std::string& msg) {
    if (has("verbose") || has("v")) {
        std::cout << colors::gray << msg << colors::reset << std::endl;
    }
}

void help(const std::string& prog_name, const std::string& usage) {
    std::cout << "Usage: " << prog_name << " " << usage << std::endl;
    std::cout << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  -h, --help     Show this help message" << std::endl;
    std::cout << "  -v, --verbose  Enable debug output" << std::endl;
}

} 