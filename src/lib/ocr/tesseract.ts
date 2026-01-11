import { createWorker } from 'tesseract.js';

export interface ScanResult {
    text: string;
    confidence: number;
}

export class OcrService {
    static async scanImage(fileObj: File | Blob): Promise<ScanResult> {
        // Convert Blob/File to base64 or URL
        const imageUrl = URL.createObjectURL(fileObj);

        const worker = await createWorker('fra');
        const ret = await worker.recognize(imageUrl);
        await worker.terminate();

        // Cleanup URL
        URL.revokeObjectURL(imageUrl);

        return {
            text: ret.data.text,
            confidence: ret.data.confidence
        };
    }

    static async scanBase64(base64Image: string): Promise<ScanResult> {
        const worker = await createWorker('fra');
        const ret = await worker.recognize(base64Image);
        await worker.terminate();

        return {
            text: ret.data.text,
            confidence: ret.data.confidence
        };
    }
}
