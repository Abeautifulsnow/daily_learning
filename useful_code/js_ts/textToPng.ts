declare global {
  interface CanvasRenderingContext2D {
    wrapText(
      this: CanvasRenderingContext2D,
      text: string,
      x: number,
      y: number,
      maxWidth: number,
      lineHeight: number
    ): void;
  }
}

export {};

// 为CanvasRenderingContext2D自定义字符串换行方法
CanvasRenderingContext2D.prototype.wrapText = function (
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number
) {
  if (typeof text != "string" || typeof x != "number" || typeof y != "number") {
    return;
  }

  const context = this;
  const canvas = context.canvas;

  if (typeof maxWidth == "undefined") {
    maxWidth = (canvas && canvas.width) || 300;
  }
  if (typeof lineHeight == "undefined") {
    lineHeight =
      (canvas && parseInt(window.getComputedStyle(canvas).lineHeight)) ||
      parseInt(window.getComputedStyle(document.body).lineHeight);
  }

  // 字符分隔为数组
  const arrText = text.split("");
  let line = "";

  for (let n = 0; n < arrText.length; n++) {
    const testLine = line + arrText[n];
    const metrics = context.measureText(testLine);
    const testWidth = metrics.width;
    if (testWidth > maxWidth && n > 0) {
      context.fillText(line, x, y);
      line = arrText[n];
      y += lineHeight;
    } else {
      line = testLine;
    }
  }
  context.fillText(line, x, y);
};

// 文字转图片的实现类
class ConvertTextToPng {
  text: string;
  fontSize: number;
  lineHeight: number;
  canvas: HTMLCanvasElement = document.createElement("canvas");
  ctx: CanvasRenderingContext2D | null;
  constructor(
    text: string,
    fontSize: number,
    lineHeight: number,
    cwidth: number,
    cheight: number
  ) {
    this.text = text;
    this.canvas.width = cwidth;
    this.canvas.height = cheight;
    this.fontSize = fontSize;
    this.lineHeight = lineHeight;
    this.ctx = this.canvas.getContext("2d");
  }

  /**
   * 返回 base64 字符串
   * @returns 返回 base64 字符串
   */
  canvasConvertTextToPng(): string | undefined {
    const ctx = this.ctx;
    if (ctx) {
      ctx.fillStyle = "#24262e";
      ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

      ctx.font = `${this.fontSize}px Verdana`;
      // const gradient = ctx.createLinearGradient(0, 0, this.canvas.width, 0)
      // gradient.addColorStop(0, 'magenta')
      // gradient.addColorStop(0.5, 'blue')
      // gradient.addColorStop(1.0, 'red')
      // ctx.fillStyle = gradient

      const gradient = ctx.createLinearGradient(0, 0, this.canvas.width, 0);
      gradient.addColorStop(0, "green");
      gradient.addColorStop(0.5, "white");
      gradient.addColorStop(1, "pink");
      ctx.fillStyle = gradient;

      this.resizeTextRange();
      const drawHStart = this.setTextHorizontalDrawStart();
      const drawVStart = this.setTextVereticalDrawStart();
      ctx.wrapText(
        this.text,
        drawHStart,
        drawVStart,
        this.canvas.width,
        this.lineHeight
      );

      return this.canvas.toDataURL("image/png");
    }
  }

  /**
   * 返回文本的维度信息
   * @returns 返回 TextMetrics 对象
   */
  getMetrics(): TextMetrics | undefined {
    if (this.ctx) {
      const metrics = this.ctx.measureText(this.text);
      return metrics;
    }
  }

  /**
   * 获取单行最大宽度
   * @returns 获取单行最大宽度
   */
  getLineMaxWidth(): number {
    const lineMaxWidth =
      Math.floor(this.canvas.width / this.fontSize) * this.fontSize;
    return lineMaxWidth;
  }

  /**
   * 获取文本在指定canvas的宽/高内，文本最大可完全看到的行数
   * @returns 获取文本在指定canvas的宽/高内，文本最大可完全看到的行数
   */
  getTextMaxLineNums(): number | undefined {
    let maxLines: number | undefined;
    const metrics = this.getMetrics();
    if (metrics) {
      const lineMaxWidth = this.getLineMaxWidth();
      const totalTextWidth = metrics.width;
      maxLines = Math.ceil(totalTextWidth / lineMaxWidth);

      return maxLines;
    }
  }

  /**
   * 文本水平居中的起始位置
   * @returns 文本水平居中的起始位置
   */
  setTextHorizontalDrawStart(): number {
    let startPositon = 0;
    const metrics = this.getMetrics();
    if (metrics) {
      if (metrics.width < this.canvas.width) {
        startPositon = Math.floor((this.canvas.width - metrics.width) / 2);
      } else {
        const lineMaxWidth = this.getLineMaxWidth();
        startPositon = (this.canvas.width - lineMaxWidth) / 2;
      }
    }
    return startPositon;
  }

  /**
   * 文本垂直居中的起始位置
   * @returns 文本垂直居中的起始位置
   */
  setTextVereticalDrawStart(): number {
    let startPositon: number = this.fontSize;
    const metrics = this.getMetrics();
    if (metrics) {
      const textMaxLines = this.getTextMaxLineNums();
      if (textMaxLines) {
        startPositon =
          (this.canvas.height - textMaxLines * this.lineHeight) / 2 +
          this.fontSize;
      }
    }

    return startPositon;
  }

  /**
   * 将 base64字符串 转为 File 对象
   * @param dataurl base64字符串
   * @param filename 文件名字
   * @returns File对象
   */
  dataURLtoFile(dataurl: string, filename: string): File {
    const arr = dataurl.split(","),
      mime = arr[0]?.match(/:(.*?);/)?.[1],
      bstr = window.atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    const fileSuffix = mime?.split("/")[1];
    if (fileSuffix) {
      filename = filename.endsWith(fileSuffix)
        ? filename
        : filename + `.${fileSuffix}`;
    }

    return new File([u8arr], filename, { type: mime });
  }

  // 当文本过多的时候，自适应文本大小和行高
  resizeTextRange() {
    const metrics = this.getMetrics();
    if (metrics) {
      const textWidth = metrics.width;
      while (
        textWidth / this.canvas.width >=
        this.canvas.width / this.lineHeight - 1
      ) {
        this.fontSize--;
        this.lineHeight -= 1.5;

        if (this.lineHeight < this.fontSize) {
          this.lineHeight = this.fontSize + 1;
        }
      }
    }
  }
}
