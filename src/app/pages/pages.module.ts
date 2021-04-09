import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NgxDropzoneModule } from 'ngx-dropzone';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AugmentationComponent } from './data/augmentation/augmentation.component';
import { UploadComponent } from './data/upload/upload.component';
import { PagesRoutingModule } from './pages-routing.module';
import { PagesComponent } from './pages.component';
import { GalleryComponent } from './data/gallery/gallery.component';
import { BottomcarouselComponent } from './data/bottomcarousel/bottomcarousel.component';
import { TopcarouselComponent } from './data/topcarousel/topcarousel.component';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSliderModule} from '@angular/material/slider';
import { MatCheckboxModule} from '@angular/material/checkbox';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatSlideToggleModule} from '@angular/material/slide-toggle'
import { CarouselComponent } from './data/carousel/carousel.component';
import { ControlsComponent } from './data/controls/controls.component';
import { DialogModule } from '../extra-components/dialog/dialog.module';
import {MatSelectModule} from '@angular/material/select';
import { PipelineComponent } from './data/pipeline/pipeline.component';
import { DataVisualizationComponent } from './data/data-visualization/data-visualization.component';
import {MatCardModule} from '@angular/material/card';
import { CropComponent } from './data/crop/crop.component';
import { DataComponent } from './data/data.component';
import { NetworkComponent } from './network/network.component';
import { ResultsComponent } from './results/results.component';
import { TrainComponent } from './network/train/train.component';
import { ModifyComponent } from './network/modify/modify.component';
import { DisplayComponent } from './network/display/display.component';
import { MatTabsModule } from '@angular/material/tabs';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { DrawerRailModule } from 'angular-material-rail-drawer';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { EmbeddingsComponent } from './results/embeddings/embeddings.component';
import { WrongResultsComponent } from './results/wrong-results/wrong-results.component';
import { SuggestionsComponent } from './results/suggestions/suggestions.component';
import { CustomDropdownComponent } from '../extra-components/custom-dropdown/custom-dropdown.component';
import {MatTooltipModule} from '@angular/material/tooltip';

import { NgApexchartsModule }  from 'ng-apexcharts';
import {IvyCarouselModule} from 'angular-responsive-carousel';
import { ImagesDialogComponent } from './data/data-visualization/images-dialog/images-dialog.component';
import { ResultService } from './results/results.service';
import { NgxSpinnerModule } from "ngx-spinner";
import {MatTableModule} from '@angular/material/table';
import { HomeComponent } from './home/home.component';
@NgModule({
  declarations: [AugmentationComponent, UploadComponent, PagesComponent, GalleryComponent, BottomcarouselComponent, TopcarouselComponent, CarouselComponent, ControlsComponent, PipelineComponent, DataVisualizationComponent, CropComponent, DataComponent, NetworkComponent, ResultsComponent, TrainComponent, ModifyComponent, DisplayComponent, EmbeddingsComponent, WrongResultsComponent, SuggestionsComponent, CustomDropdownComponent, ImagesDialogComponent, HomeComponent],
  imports: [
    CommonModule,
    PagesRoutingModule,
    NgxDropzoneModule,
    ReactiveFormsModule,
    HttpClientModule,
    CommonModule,
    FormsModule,

    // Materials
    MatInputModule,
    MatButtonModule,
    MatExpansionModule,
    MatIconModule,
    MatSliderModule,
    MatCheckboxModule,
    MatSlideToggleModule,
    MatSelectModule,
    MatCardModule,
    MatTabsModule,
    MatFormFieldModule,
    MatSnackBarModule,
    MatSidenavModule,
    MatListModule,
    DrawerRailModule,
    MatTooltipModule,
    MatTableModule,

    // Extra
    DialogModule,
    NgApexchartsModule,
    IvyCarouselModule,
    NgxSpinnerModule
  ],
  providers: [ResultService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  // exports: [SafeHtml],
})
export class PagesModule { }
