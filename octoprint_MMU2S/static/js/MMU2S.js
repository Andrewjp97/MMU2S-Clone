/*
 * View model for MMU2S
 *
 * Author: Andrew Paterson
 * License: AGPLv3
 */
$(function() {
    function Mmu2sViewModel(parameters) {
        var self = this;
        self.currentMaterial = 99;
        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
        self.createFilamentControls = function() {
          $("#canvas_container").after(
            '<div id="filamentControls">' +
              '<div class="main">' +
                gettext("Load Filament") +
                ' <div class="btn-group action-buttons">' +
                  '<div class="btn btn-mini unloadAllFilament" title="' + gettext("Unload All Filament") + '">' +
                  '<i class="fa"></i>' + gettext("Unload All") + '</div>' +
                  '<div class="btn btn-mini loadFilamentOne" title="' + gettext("Load Filament One") + '">' +
                  '<i class="fa"></i>' + gettext("Load Filament 1") + '</div>' +
                  '<div class="btn btn-mini loadFilamentTwo" title="' + gettext("Load Filament Two") + '">' +
                  '<i class="fa"></i>' + gettext("Load Filament 2") + '</div>' +
                '</div>' +
              '</div>' +
            '</div>'
          );
        }

        self.createFilamentControls;

        self.$filamentControls = $("#filamentControls .btn");

        self.$filamentControls.click(function(){
          var $button = $(this);

          if ($button.hasClass("unloadAllFilament")){
            self.unloadAllFilament;
          }
          else if ($button.hasClass("loadFilamentOne")){
            self.loadFilamentOne;
          }
          else if ($button.hasClass("loadFilamentTwo")){
            self.loadFilamentTwo;
          }
        });

        self.unloadAllFilament = function(){

        }

        self.loadFilamentOne = function() {
          if (self.currentMaterial == 99){
            // Current material is unknown
            self.unloadAllFilament;
            self.currentMaterial = 101;
          }
          else if (self.currentMaterial == 101){
            // Verified no materials loaded
            // No action needed
          }
          else if (self.currentMaterial == 1){
            // Material 1 Already loaded
            return;
          }
          else {
            self.unloadMaterial(self.currentMaterial);
          }
          // Load Filament One Starting here

          // #TODO

          self.currentMaterial = 1;

        }

        self.unloadMaterial = function(material){

        }

        self.loadFilamentTwo = function() {

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
        elements: [#tab_plugin_MMU2S]
    });
});
