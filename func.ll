; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"x" = internal global i32 undef
define i32 @"sqr"(i32 %"x") 
{
sqr.block:
  %".3" = alloca i32
  store i32 %"x", i32* %".3"
  %"res" = alloca i32
  %".5" = load i32, i32* %".3"
  %".6" = load i32, i32* %".3"
  %".7" = mul i32 %".5", %".6"
  store i32 %".7", i32* %"res"
  %".9" = load i32, i32* %"res"
  ret i32 %".9"
}

define i32 @"main"() 
{
main.block:
  store i32 10, i32* @"x"
  %".3" = load i32, i32* @"x"
  %".4" = getelementptr inbounds [4 x i8], [4 x i8]* @".str_id_1", i32 0, i32 0
  %".5" = load i32, i32* @"x"
  %".6" = call i32 @"sqr"(i32 %".5")
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %".6")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...) 

@".str_id_1" = constant [4 x i8] c"%d\0a\00"