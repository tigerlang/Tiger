// ============================================================
// ============================================================
namespace tiger_gui {
static void button(const std::string& text) {
    int id = g_ctrlId++;
    int y = g_nextY;
    g_nextY += 40;
    
    HWND hBtn = CreateWindowW(
        L"BUTTON", to_wide(text).c_str(),
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        20, y, 160, 30,
        g_hwnd, (HMENU)(intptr_t)id,
        GetModuleHandleW(nullptr), nullptr);
    
    g_buttons.push_back({id, to_wide(text), hBtn, nullptr});
}
} 