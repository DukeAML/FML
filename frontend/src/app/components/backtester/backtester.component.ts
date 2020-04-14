import { Component, OnInit } from '@angular/core';
import { BacktesterDialogComponent } from '../backtester-dialog/backtester-dialog.component'
import { DataService } from '../../services/data.service';
import { MatButton } from '@angular/material'
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


@Component({
  selector: 'app-backtester',
  templateUrl: './backtester.component.html',
  styleUrls: ['./backtester.component.css']
})
export class BacktesterComponent implements OnInit {

  params:any[];


  constructor(private dataService:DataService, public dialog:MatDialog) { }

  ngOnInit() {
  }

  openDialog(): void {
    console.log('opened');
    const dialogRef = this.dialog.open(BacktesterDialogComponent, {
      width: '250px',
      hasBackdrop:false
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed, result was', result);
    });
  }

}
