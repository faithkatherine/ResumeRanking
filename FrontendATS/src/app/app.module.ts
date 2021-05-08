import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AccountComponent } from './account/account.component';
import { JobsComponent } from './jobs/jobs.component';

@NgModule({

  imports: [
    BrowserModule,
    AppRoutingModule
  ],

  declarations: [
    AppComponent,
    AccountComponent,
    JobsComponent
  ],

  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
