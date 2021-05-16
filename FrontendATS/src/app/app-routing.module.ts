import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AccountComponent } from './account/account.component';
import { HomeComponent } from './home/home.component';
import { JobPostComponent } from './job-post/job-post.component';
import { ResumePostComponent } from './resume-post/resume-post.component';

const routes: Routes = [
  {path:'home', component:HomeComponent},
  {path:'account', component:AccountComponent},
  {path:'jobpost', component:JobPostComponent},
  {path:'resumepost', component:ResumePostComponent},
  {path:'' , redirectTo:'home', pathMatch: 'full'}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
