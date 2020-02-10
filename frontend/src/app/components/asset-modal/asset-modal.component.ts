import { Component, OnInit, Inject } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


@Component({
  selector: 'app-asset-modal',
  templateUrl: './asset-modal.component.html',
  styleUrls: ['./asset-modal.component.css']
})
export class AssetModalComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) private data:any) { }

  ngOnInit() {
    
  }

}
