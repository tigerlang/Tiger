// ============================================================
// ============================================================
namespace tiger_gui {
static void label(const std::string& text) {
    int y = g_nextY;
    g_nextY += 40;
    
    HWND hLbl = CreateWindowW(
        L"STATIC", to_wide(text).c_str(),
        WS_VISIBLE | WS_CHILD,
        20, y, 160, 30,
        g_hwnd, (HMENU)(intptr_t)(g_ctrlId++),
        GetModuleHandleW(nullptr), nullptr);
}
} 