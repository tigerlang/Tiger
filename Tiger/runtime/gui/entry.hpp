// ============================================================
// ============================================================
namespace tiger_gui {
static std::string g_entry_text = "";

static std::string get_entry(int id) {
    char buf[512];
    HWND hEdit = GetDlgItem(g_hwnd, id);
    if (hEdit) {
        GetWindowTextA(hEdit, buf, 512);
        return std::string(buf);
    }
    return "";
}

static void entry(const std::string& name) {
    int id = g_ctrlId++;
    int y = g_nextY;
    g_nextY += 30;
    
    HWND hEdit = CreateWindowW(
        L"EDIT", L"",
        WS_VISIBLE | WS_CHILD | WS_BORDER | ES_LEFT,
        20, y, 160, 25,
        g_hwnd, (HMENU)(intptr_t)id,
        GetModuleHandleW(nullptr), nullptr);
}
} 