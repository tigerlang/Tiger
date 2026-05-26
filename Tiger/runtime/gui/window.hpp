// ============================================================
// ============================================================
namespace tiger_gui {
static void window(const std::string& title, int w, int h) {
    HINSTANCE hInst = GetModuleHandleW(nullptr);
    const wchar_t* cls = L"TigerWindow";
    WNDCLASSW wc = {};
    wc.lpfnWndProc   = WndProc;
    wc.hInstance     = hInst;
    wc.lpszClassName = cls;
    wc.hCursor       = LoadCursor(nullptr, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    RegisterClassW(&wc);
    g_hwnd = CreateWindowExW(
        0, cls, to_wide(title).c_str(),
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, w, h,
        nullptr, nullptr, hInst, nullptr);
    ShowWindow(g_hwnd, SW_SHOW);
    UpdateWindow(g_hwnd);
    g_nextY = 20;
    g_running = true;
}
} 