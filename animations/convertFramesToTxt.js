import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Import frames from frames.js
import { frames } from './frames.js';

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Function to validate directory name
function validateDirectoryName(name) {
  // Check for invalid characters (spaces, special characters that might cause issues)
  const invalidChars = /[<>:"/\\|?*\s]/;
  if (invalidChars.test(name)) {
    return false;
  }
  // Check if name is not empty
  if (!name.trim()) {
    return false;
  }
  return true;
}

// Function to prompt user for directory name
function promptForDirectoryName() {
  return new Promise((resolve) => {
    rl.question('請輸入動畫資料夾名稱 (不能包含空格或特殊字元): ', (answer) => {
      const trimmedAnswer = answer.trim();
      if (validateDirectoryName(trimmedAnswer)) {
        resolve(trimmedAnswer);
      } else {
        console.log('❌ 無效的資料夾名稱！請避免使用空格和特殊字元 (<>:"/\\|?*)');
        promptForDirectoryName().then(resolve);
      }
    });
  });
}

// Main execution
async function main() {
  try {
    console.log('🎬 Frame to TXT 轉換工具');
    console.log(`📊 共找到 ${frames.length} 個影格`);

    const directoryName = await promptForDirectoryName();
    const outputDir = path.join(__dirname, directoryName);

    // Ensure the output directory exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir);
      console.log(`📁 已建立資料夾: ${directoryName}`);
    } else {
      console.log(`📁 使用現有資料夾: ${directoryName}`);
    }

    // Convert each frame to a .txt file
    console.log('🔄 開始轉換 Frames...');
    frames.forEach((frame, index) => {
      const fileName = `frame_${index + 1}.txt`;
      const filePath = path.join(outputDir, fileName);

      fs.writeFileSync(filePath, frame, 'utf8');
      console.log(`✅ 已儲存: ${fileName}`);
    });

    console.log(`🎉 所有 Frames 已成功轉換為 .txt 檔案！`);
    console.log(`📍 檔案位置: ${outputDir}`);

  } catch (error) {
    console.error('❌ 轉換過程中發生錯誤:', error.message);
  } finally {
    rl.close();
  }
}

main(); 
