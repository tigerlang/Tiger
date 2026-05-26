// ============================================================
// ============================================================

namespace tiger_gui {

static int button_ex(int x, int y, int w, int h, const std::string& text,
                   const std::string& bgColorStr, const std::string& textColorStr, std::function<void()> callback) {
    int id = g_ctrlId++;
    COLORREF bgColor = parse_color(bgColorStr);
    COLORREF textColor = parse_color(textColorStr);
    
    HWND hBtn = CreateWindowW(
        L"BUTTON", to_wide(text).c_str(),
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_OWNERDRAW,
        x, y, w, h,
        g_hwnd, (HMENU)(intptr_t)id,
        GetModuleHandleW(nullptr), nullptr);
    
    g_buttons.push_back({id, to_wide(text), hBtn, callback, bgColor, textColor});
    return id;
}

static int button_colored(const std::string& text, const std::string& bgColorStr, const std::string& textColorStr, 
                         std::function<void()> callback) {
    int id = g_ctrlId++;
    int y = g_nextY;
    g_nextY += 40;
    COLORREF bgColor = parse_color(bgColorStr);
    COLORREF textColor = parse_color(textColorStr);
    
    HWND hBtn = CreateWindowW(
        L"BUTTON", to_wide(text).c_str(),
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_OWNERDRAW,
        20, y, 160, 30,
        g_hwnd, (HMENU)(intptr_t)id,
        GetModuleHandleW(nullptr), nullptr);
    
    g_buttons.push_back({id, to_wide(text), hBtn, callback, bgColor, textColor});
    return id;
}

} 