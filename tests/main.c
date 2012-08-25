/*
 * main.c
 *
 *  Created on: 7 May 2012
 *      Author: robomotic
 */


//******************************************************************************
//  eZ430 chronos hello world
//  Description: initializes lcd module and shows the string 'hi earth' on the
//               lcd display becuase 'hello world' is too long
//  Author: Felix Genicio
//******************************************************************************

#include  "cc430x613x.h"
#include <string.h>

void main(void)
{
	unsigned char * lcdmem;

    // Clear entire display memory
	LCDBMEMCTL |= LCDCLRBM + LCDCLRM;

	// LCD_FREQ = ACLK/16/8 = 256Hz
	// Frame frequency = 256Hz/4 = 64Hz, LCD mux 4, LCD on
	LCDBCTL0 = (LCDDIV0 + LCDDIV1 + LCDDIV2 + LCDDIV3) | (LCDPRE0 + LCDPRE1) | LCD4MUX | LCDON;

	// LCB_BLK_FREQ = ACLK/8/4096 = 1Hz
	LCDBBLKCTL = LCDBLKPRE0 | LCDBLKPRE1 | LCDBLKDIV0 | LCDBLKDIV1 | LCDBLKDIV2 | LCDBLKMOD0;

	// I/O to COM outputs
	P5SEL |= (BIT5 | BIT6 | BIT7);
	P5DIR |= (BIT5 | BIT6 | BIT7);

	// Activate LCD output
	LCDBPCTL0 = 0xFFFF;  // Select LCD segments S0-S15
	LCDBPCTL1 = 0x00FF;  // Select LCD segments S16-S22

	// LCD_B Base Address is 0A00H page 30 y in SALS554 document
	// show 'h'
	lcdmem 	= (unsigned char *)0x0A21;
	*lcdmem = (unsigned char)(*lcdmem | (BIT2+BIT1+BIT6+BIT0));
	// show 'i'
	lcdmem 	= (unsigned char *)0x0A22;
	*lcdmem = (unsigned char)(*lcdmem | (BIT2));
	// show 'E'
	lcdmem 	= (unsigned char *)0x0A2B;
	*lcdmem = (unsigned char)(*lcdmem | (BIT4+BIT5+BIT6+BIT0+BIT3));
	// show 'A'
	lcdmem 	= (unsigned char *)0x0A2A;
	*lcdmem = (unsigned char)(*lcdmem | (BIT0+BIT1+BIT2+BIT4+BIT5+BIT6));
	// show 'r'
	lcdmem 	= (unsigned char *)0x0A29;
	*lcdmem = (unsigned char)(*lcdmem | (BIT6+BIT5));
	// show 't'
	lcdmem 	= (unsigned char *)0x0A28;
	*lcdmem = (unsigned char)(*lcdmem | (BIT4+BIT5+BIT6+BIT3));
	// show 'h'
	lcdmem 	= (unsigned char *)0x0A27;
	*lcdmem = (unsigned char)(*lcdmem | (BIT4+BIT5+BIT6+BIT2));

	for(char i=0;i<23;i++)
	{
	  __no_operation();  // For debugger
	}
}
