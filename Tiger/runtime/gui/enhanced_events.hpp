// ============================================================
// ============================================================

namespace tiger_gui {

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    switch (msg) {
    case WM_COMMAND: {
        int id = LOWORD(wp);
        int code = HIWORD(wp);
        for (auto& b : g_buttons) {
            if (b.id == id && code == BN_CLICKED) {
                if (b.onClick) b.onClick();
            }
        }
        break;
    }
    case WM_DRAWITEM: {
        LPDRAWITEMSTRUCT pDIS = (LPDRAWITEMSTRUCT)lp;
        for (auto& b : g_buttons) {
            if (pDIS->CtlID == b.id) {
                HDC hdc = pDIS->hDC;
                RECT rc = pDIS->rcItem;
                HBRUSH hbr = CreateSolidBrush(b.bgColor);
                FillRect(hdc, &rc, hbr);
                SetBkMode(hdc, TRANSPARENT);
                SetTextColor(hdc, b.textColor);
                DrawTextW(hdc, b.text.c_str(), -1, &rc, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
                DeleteObject(hbr);
                return TRUE;
            }
        }
        break;
    }
    case WM_CLOSE:
        g_running = false;
        DestroyWindow(hwnd);
        return 0;
    }
    return DefWindowProcW(hwnd, msg, wp, lp);
}

} 