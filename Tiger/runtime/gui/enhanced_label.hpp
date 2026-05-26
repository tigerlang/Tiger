// ============================================================
// ============================================================

namespace tiger_gui {

static void label_ex(int x, int y, int w, int h, const std::string& text, 
                   const std::string& textColorStr, const std::string& bgColorStr) {
    COLORREF textColor = parse_color(textColorStr);
    COLORREF bgColor = parse_color(bgColorStr);
    
    HWND hLbl = CreateWindowW(
        L"STATIC", to_wide(text).c_str(),
        WS_VISIBLE | WS_CHILD,
        x, y, w, h,
        g_hwnd, (HMENU)(intptr_t)(g_ctrlId++),
        GetModuleHandleW(nullptr), nullptr);
    
    g_labels.push_back({hLbl, textColor, bgColor});
}

static void label_colored(const std::string& text, const std::string& textColorStr, const std::string& bgColorStr) {
    int y = g_nextY;
    g_nextY += 40;
    COLORREF textColor = parse_color(textColorStr);
    COLORREF bgColor = parse_color(bgColorStr);
    
    HWND hLbl = CreateWindowW(
        L"STATIC", to_wide(text).c_str(),
        WS_VISIBLE | WS_CHILD,
        20, y, 160, 30,
        g_hwnd, (HMENU)(intptr_t)(g_ctrlId++),
        GetModuleHandleW(nullptr), nullptr);
    
    g_labels.push_back({hLbl, textColor, bgColor});
}

} 