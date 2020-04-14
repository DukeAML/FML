import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { BotComponent } from './components/bot/bot.component';
import { HttpClientModule } from '@angular/common/http';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToolbarComponent } from './components/toolbar/toolbar.component';
import { AboutComponent } from './components/about/about.component';
import { MatButtonModule, MatChipsModule, MatDatepickerModule, MatDialogModule, MatExpansionModule, MatFormFieldModule, MatIconModule, MatInputModule, MatNativeDateModule, MatOptionModule, MatProgressSpinner, MatSelectModule, MatSliderModule, MatToolbarModule, MatTooltipModule, MatProgressSpinnerModule, MatButton } from '@angular/material';
import { AssetModalComponent } from './components/asset-modal/asset-modal.component';
import { PerformancePaneComponent } from './components/performance-pane/performance-pane.component';
import { DashboardGraphsComponent } from './components/dashboard-graphs/dashboard-graphs.component';
import { IndicatorsComponent } from './components/indicators/indicators.component';
import { IndicatorComponent } from './components/indicator/indicator.component';
import { TopTickersComponent } from './components/top-tickers/top-tickers.component';
import { TickerComponent } from './components/ticker/ticker.component';
import { BacktesterComponent } from './components/backtester/backtester.component';
import { BacktesterDialogComponent } from './components/backtester-dialog/backtester-dialog.component';



@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    BotComponent,
    ToolbarComponent,
    AboutComponent,
    AssetModalComponent,
    PerformancePaneComponent,
    DashboardGraphsComponent,
    IndicatorsComponent,
    IndicatorComponent,
    TopTickersComponent,
    TickerComponent,
    BacktesterComponent,
    BacktesterDialogComponent,
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatButtonModule,
    MatChipsModule,
    MatDialogModule,
    MatDatepickerModule,
    MatExpansionModule,
    MatIconModule,
    MatInputModule,
    MatNativeDateModule,
    MatToolbarModule, 
    MatTooltipModule,
    MatFormFieldModule,
    MatOptionModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatSliderModule, 
    NgxChartsModule
  ],
  entryComponents: [
    BacktesterDialogComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
