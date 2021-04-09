import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AugmentationComponent } from './data/augmentation/augmentation.component';
import { DataVisualizationComponent } from './data/data-visualization/data-visualization.component';
import { GalleryComponent } from './data/gallery/gallery.component';
import { PagesComponent } from './pages.component';
import { PipelineComponent } from './data/pipeline/pipeline.component';
import { UploadComponent } from './data/upload/upload.component';
import { DataComponent } from './data/data.component';
import { NetworkComponent } from './network/network.component';
import { ResultsComponent } from './results/results.component';
import { TrainComponent } from './network/train/train.component';
import { ModifyComponent } from './network/modify/modify.component';
import { DisplayComponent } from './network/display/display.component';
import { EmbeddingsComponent } from './results/embeddings/embeddings.component';
import { WrongResultsComponent } from './results/wrong-results/wrong-results.component';
import { SuggestionsComponent } from './results/suggestions/suggestions.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  {
    path: '',
    component: PagesComponent,
    children: [
      {
        path: 'data',
        component: DataComponent,
        children: [
          {
            path: 'upload', component: UploadComponent,
          },
          {
            path: 'gallery', component: GalleryComponent,
          },
          {
            path: 'transformation', component: AugmentationComponent,
          },
          {
            path: 'pipeline', component: PipelineComponent,
          },
          {
            path: 'visualize', component: DataVisualizationComponent,
          },
          {
            path: '**', redirectTo: 'upload',
          },
        ],
      },
      {
        path: 'network',
        component: NetworkComponent,
        children: [
          {
            path: 'train', component: TrainComponent,
          },
          {
            path: 'modify', component: ModifyComponent,
          },
          {
            path: 'display', component: DisplayComponent,
          },
          {
            path: '**', redirectTo: 'display',
          },
        ],
      },
      {
        path: 'results',
        component: ResultsComponent,
        children: [
          {
            path: 'embeddings', component: EmbeddingsComponent,
          },
          {
            path: 'wrongres', component: WrongResultsComponent,
          },
          {
            path: 'suggestions', component: SuggestionsComponent,
          },
          {
            path: '**', redirectTo: 'embeddings',
          },
        ],
      },
      {path: 'home', component: HomeComponent},
      {
        path : '**',
        redirectTo : 'home',
      }
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule { }
