import { Component, OnInit } from '@angular/core';
import { ResumePostService } from '../services/resume-post.service';

@Component({
  selector: 'app-resume-post',
  templateUrl: './resume-post.component.html',
  styleUrls: ['./resume-post.component.css']
})
export class ResumePostComponent implements OnInit {

  public posts;
  constructor(private ResumePostService:ResumePostService) { }

  ngOnInit(): void {
    this.getPosts();
  }

  getPosts() {
    this.ResumePostService.list().subscribe(
      // the first argument is a function which runs on success
      data => {
        this.posts = data;
        for (let post of this.posts) {
          post.date_updated = new Date(post.date_updated);
          let url = "http://127.0.0.1:8000/";

        }

      },
      err => console.error(err),
      () => console.log('done loading posts')

    );
  }
}
