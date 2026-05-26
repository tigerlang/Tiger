// ============================================================
// ============================================================
#ifndef UNICODE
#define UNICODE
#endif
#include <windows.h>
#include <functional>
#include <string>
#include <vector>

namespace tiger_gui {

HWND  g_hwnd    = nullptr;
int   g_ctrlId  = 1000;
int   g_nextY   = 20;
int   g_nextX   = 20;
bool  g_running = false;

const COLORREF COLOR_WHITE    = RGB(255, 255, 255);
const COLORREF COLOR_BLACK    = RGB(0, 0, 0);
const COLORREF COLOR_RED      = RGB(255, 0, 0);
const COLORREF COLOR_GREEN    = RGB(0, 255, 0);
const COLORREF COLOR_BLUE     = RGB(0, 0, 255);
const COLORREF COLOR_YELLOW   = RGB(255, 255, 0);
const COLORREF COLOR_CYAN     = RGB(0, 255, 255);
const COLORREF COLOR_MAGENTA  = RGB(255, 0, 255);
const COLORREF COLOR_GRAY     = RGB(128, 128, 128);
const COLORREF COLOR_LIGHTGRAY= RGB(211, 211, 211);
const COLORREF COLOR_ORANGE   = RGB(255, 165, 0);

struct LabelInfo {
    HWND hwnd;
    COLORREF textColor;
    COLORREF bgColor;
};

struct ButtonInfo {
    int id;
    std::wstring text;
    HWND hwnd;
    std::function<void()> onClick;
    COLORREF bgColor;
    COLORREF textColor;
};

std::vector<ButtonInfo> g_buttons;
std::vector<LabelInfo>  g_labels;

std::wstring to_wide(const std::string& s) {
    if (s.empty()) return L"";
    int n = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, nullptr, 0);
    std::wstring ws(n, 0);
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, &ws[0], n);
    ws.resize(n - 1);
    return ws;
}

COLORREF parse_color(const std::string& s) {
    if (s == "white")  return COLOR_WHITE;
    if (s == "black")  return COLOR_BLACK;
    if (s == "red")    return COLOR_RED;
    if (s == "green")  return COLOR_GREEN;
    if (s == "blue")   return COLOR_BLUE;
    if (s == "yellow") return COLOR_YELLOW;
    if (s == "cyan")   return COLOR_CYAN;
    if (s == "magenta")return COLOR_MAGENTA;
    if (s == "gray")   return COLOR_GRAY;
    if (s == "orange") return COLOR_ORANGE;
    return COLOR_WHITE;
}

} 