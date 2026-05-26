// ============================================================
// ============================================================
#include <filesystem>
#include <fstream>
#include <vector>
#include <string>
#include <iostream>

namespace tiger_files {

namespace fs = std::filesystem;

bool exists(const std::string& path) {
    return fs::exists(path);
}

void create_dir(const std::string& path) {
    std::error_code ec;
    bool created = fs::create_directory(path, ec);
    if (ec && !fs::exists(path)) {
        std::cerr << "DEBUG: create_dir error: " << ec.message() << " for " << path << std::endl;
        throw std::runtime_error("files.create_dir: failed to create directory: " + path);
    }
}

void create_file(const std::string& path) {
    std::ofstream ofs(path);
    if (!ofs) {
        throw std::runtime_error("files.create_file: failed to create file: " + path);
    }
    ofs.close();
}

void remove_dir(const std::string& path) {
    std::error_code ec;
    if (!fs::remove(path, ec)) {
        throw std::runtime_error("files.remove_dir: failed to remove directory: " + path);
    }
}

void remove_file(const std::string& path) {
    std::error_code ec;
    if (!fs::remove(path, ec)) {
        throw std::runtime_error("files.remove_file: failed to remove file: " + path);
    }
}

std::vector<std::string> list_dir(const std::string& path) {
    std::vector<std::string> result;
    std::error_code ec;
    for (const auto& entry : fs::directory_iterator(path, ec)) {
        if (!ec) {
            result.push_back(entry.path().filename().string());
        }
    }
    return result;
}

std::string read(const std::string& path) {
    std::ifstream ifs(path);
    if (!ifs) {
        throw std::runtime_error("files.read: failed to open file for reading: " + path);
    }
    return std::string((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
}

void write(const std::string& path, const std::string& content) {
    std::ofstream ofs(path);
    if (!ofs) {
        throw std::runtime_error("files.write: failed to open file for writing: " + path);
    }
    ofs << content;
    ofs.close();
}

} 