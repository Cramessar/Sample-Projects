import wx
import requests

class DNDApp(wx.Frame):
    def __init__(self, parent, title):
        super(DNDApp, self).__init__(parent, title=title, size=(500, 600))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Number of Players
        self.players_label = wx.StaticText(panel, label="Select the Number of Players:")
        self.players_choice = wx.Choice(panel, choices=[str(i) for i in range(1, 11)])
        self.players_choice.SetSelection(0)

        # Class Selection
        self.class_label = wx.StaticText(panel, label="Select Classes for this Run:")
        self.classes = ['Warrior', 'Mage', 'Ranger', 'Rogue', 'Paladin', 'Druid']
        self.class_checkboxes = []
        for class_name in self.classes:
            checkbox = wx.CheckBox(panel, label=class_name)
            self.class_checkboxes.append(checkbox)

        # Starting Level
        self.level_label = wx.StaticText(panel, label="Enter Starting Level for Players:")
        self.level_input = wx.SpinCtrl(panel, value='1', min=1, max=20)

        # Fetch Button
        self.fetch_button = wx.Button(panel, label="Start Campaign")
        self.fetch_button.Bind(wx.EVT_BUTTON, self.start_campaign)

        # Result Output
        self.result_label = wx.StaticText(panel, label="Selected Options will appear here.", size=(450, -1))
        self.result_label.Wrap(450)

        # Add Widgets to Layout
        vbox.Add(self.players_label, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.players_choice, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add(self.class_label, flag=wx.LEFT | wx.TOP, border=10)
        for checkbox in self.class_checkboxes:
            vbox.Add(checkbox, flag=wx.LEFT, border=20)

        vbox.Add(self.level_label, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.level_input, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add(self.fetch_button, flag=wx.LEFT | wx.TOP, border=20)
        vbox.Add(self.result_label, flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=20)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def start_campaign(self, event):
        # Retrieve the selected number of players
        num_players = self.players_choice.GetStringSelection()

        # Retrieve selected classes
        selected_classes = [chk.GetLabel() for chk in self.class_checkboxes if chk.IsChecked()]

        # Retrieve starting level
        starting_level = self.level_input.GetValue()

        # Show a summary of selected options
        if not selected_classes:
            self.result_label.SetLabel("Please select at least one class.")
        else:
            result = (
                f"Number of Players: {num_players}\n"
                f"Selected Classes: {', '.join(selected_classes)}\n"
                f"Starting Level: {starting_level}"
            )
            self.result_label.SetLabel(result)
            self.result_label.Wrap(450)

if __name__ == "__main__":
    app = wx.App(False)
    frame = DNDApp(None, "D&D Campaign Setup")
    app.MainLoop()
