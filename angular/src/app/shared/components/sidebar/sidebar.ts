import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
@Component({
  selector: 'app-sidebar',
  imports: [RouterModule, MatIconModule, MatListModule],
  templateUrl: './sidebar.html'
})
export class Sidebar {

}
