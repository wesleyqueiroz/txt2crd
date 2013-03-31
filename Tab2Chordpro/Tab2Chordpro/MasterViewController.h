//
//  MasterViewController.h
//  Tab2Chordpro
//
//  Created by Magnus Olsson on 3/31/13.
//  Copyright (c) 2013 Magnus Olsson. All rights reserved.
//

#import <UIKit/UIKit.h>

@class DetailViewController;

@interface MasterViewController : UITableViewController

@property (strong, nonatomic) DetailViewController *detailViewController;

@end
