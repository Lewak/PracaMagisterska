from dearpygui import core, simple
from settings_window import SettingsWindow

core.enable_docking()
settingsWindow = SettingsWindow()

core.set_main_window_title("NeuronApplication")
with simple.window('MainWindow'):
    core.add_menu_bar("MenuBar")
    with simple.menu("Motyw##demo"):
        core.add_menu_item("Ciemny", callback=lambda sender, data: core.set_theme("Dark"), check=True)
        core.add_menu_item("Jasny", callback=lambda sender, data: core.set_theme("Light"), check=True)
        core.add_menu_item("Klasyczny", callback=lambda sender, data: core.set_theme("Classic"), check=True)
        core.add_menu_item("Ciemny 2", callback=lambda sender, data: core.set_theme("Dark 2"), check=True)
        core.add_menu_item("Szary", callback=lambda sender, data: core.set_theme("Grey"), check=True)
        core.add_menu_item("Ciemno-Szary", callback=lambda sender, data: core.set_theme("Dark Grey"), check=True)
        core.add_menu_item("Wisniowy", callback=lambda sender, data: core.set_theme("Cherry"), check=True)
        core.add_menu_item("Purpurowy", callback=lambda sender, data: core.set_theme("Purple"), check=True)
        core.add_menu_item("Zloty", callback=lambda sender, data: core.set_theme("Gold"), check=True)
        core.add_menu_item("Czerwony", callback=lambda sender, data: core.set_theme("Red"), check=True)
    with simple.menu("Pozycja"):
        core.add_menu_item("Zresetuj wszystko", callback=lambda sender, data: settingsWindow.reset_all())
        pass
    with simple.menu("Ukryj"):
        core.add_menu_item("Okno ustawien", callback = lambda sender, data: settingsWindow.toggle_visibility())
        core.add_menu_item("Wizualizacja sieci", callback = lambda sender, data: settingsWindow.betterVisualizer.toggle_visibility())
        core.add_menu_item("Wczytaj plik", callback = lambda sender, data: settingsWindow.importWindow.toggle_visibility())
        core.add_menu_item("Odpowiedz sieci", callback = lambda sender, data: settingsWindow.outputVisualisationWindow.toggle_visibility())
        core.add_menu_item("Historia uczenia##temp2", callback = lambda sender, data: settingsWindow.historyGraphWindow.toggle_visibility())



core.start_dearpygui(primary_window="MainWindow")

