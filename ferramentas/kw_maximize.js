for (const w of workspace.windowList()) {
    if (w.caption.indexOf("Teste da barra de titulo") !== -1) { w.setMaximize(true, true); }
}
