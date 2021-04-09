import { Component } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: []
})
export class AppComponent {
  title = 'traffic-sign-recognition';
  constructor(private matIconRegistry: MatIconRegistry, private domSanitizer: DomSanitizer){
    this.matIconRegistry.addSvgIcon(
      "my_data",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../assets/icons/folder.svg")
    );
    this.matIconRegistry.addSvgIcon(
      "my_network",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../assets/icons/pie-chart.svg")
    );
    this.matIconRegistry.addSvgIcon(
      "my_results",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../assets/icons/settings-1.svg")
    );
    this.matIconRegistry.addSvgIcon(
      "my_logo",
      this.domSanitizer.bypassSecurityTrustResourceUrl("../assets/icons/house.svg")
    );
    }
  
  ngOnInit(){
  }
}
