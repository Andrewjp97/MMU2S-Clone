/*
 * View model for MMU2S
 *
 * Author: Andrew Paterson
 * License: AGPLv3
 */
$(function() {
    function Mmu2sViewModel(parameters) {
        var self = this;
        var PLUGIN_ID = "MMU2S";

        // self.onBeforeBinding = function() {
        //   OctoPrint.get("api/plugin/" + PLUGIN_ID);
        // }
        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
        // self.createFilamentControls = function() {
        //   $("#canvas_container").after(
        //     '<div id="filamentControls">' +
        //       '<div class="main">' +
        //         gettext("Load Filament") +
        //         ' <div class="btn-group action-buttons">' +
        //           '<div class="btn btn-mini unloadAllFilament" title="' + gettext("Unload All Filament") + '">' +
        //           '<i class="fa"></i>' + gettext("Unload All") + '</div>' +
        //           '<div class="btn btn-mini loadFilamentOne" title="' + gettext("Load Filament One") + '">' +
        //           '<i class="fa"></i>' + gettext("Load Filament 1") + '</div>' +
        //           '<div class="btn btn-mini loadFilamentTwo" title="' + gettext("Load Filament Two") + '">' +
        //           '<i class="fa"></i>' + gettext("Load Filament 2") + '</div>' +
        //         '</div>' +
        //       '</div>' +
        //     '</div>'
        //   );
        // }

        //self.createFilamentControls;


        self.$filamentControls = $("#filamentControls .btn");

        self.$filamentControls.click(function(){
          var $button = $(this);

          if ($button.hasClass("unloadAllFilament")){
            self.unloadAllFilament();
            $button.css("color", "red")
          }
          else if ($button.hasClass("loadFilamentOne")){
            self.loadFilamentOne();
            $button.css("color", "green")
          }
          else if ($button.hasClass("loadFilamentTwo")){
            self.loadFilamentTwo();
          }
        });

        self.$initializationControls = $("#initializationControls .btn");

        self.$initializationControls.click(function(){
          var $button = $(this);

          if ($button.hasClass("initializeMMU2S")){
            self.initializeMMU2S();
            $button.css("color", "green")
          }
        });

        self.unloadAllFilament = function(){
          $.ajax({
                url: API_BASEURL + "plugin/" + PLUGIN_ID,
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "unloadAllFilament",
                }),
                contentType: "application/json; charset=UTF-8"
            });
            return;
        }

        self.initializeMMU2S = function(){
          $.ajax({
                url: API_BASEURL + "plugin/" + PLUGIN_ID,
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "initializeMMU2S",
                }),
                contentType: "application/json; charset=UTF-8"
            });
            return;
        }

        self.loadFilamentOne = function() {
          $.ajax({
            url: API_BASEURL + "plugin/" + PLUGIN_ID,
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                command: "loadFilament",
                material: 0
            }),
            contentType: "application/json; charset=UTF-8"
          });
          return;



        }

        self.loadFilamentTwo = function() {
          $.ajax({
            url: API_BASEURL + "plugin/" + PLUGIN_ID,
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                command: "loadFilament",
                material: 1
            }),
            contentType: "application/json; charset=UTF-8"
          });
          return;
        }

    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: Mmu2sViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_MMU2S, #tab_plugin_MMU2S, ...
        elements: ["#tab_plugin_MMU2S"]
    });
});
