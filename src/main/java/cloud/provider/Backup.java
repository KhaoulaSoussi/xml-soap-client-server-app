package cloud.provider;

import javax.jws.WebService;
import java.io.File;
import java.io.FileOutputStream;

@WebService
public class Backup {
    String folder_path;

    public String create_backup_folder(String folder_name){
        boolean is_created;
        folder_path = folder_name + "_Backup/";
        File dir = new File(folder_path);
        if(!dir.exists()) {
            is_created = dir.mkdir();
        }
        else {
            is_created = true;
        }
        String msg = "SUCCESS: " + folder_name + "_Backup" + " CREATED SUCCESSFULLY...";
        if(!is_created) {
            msg = "FAILURE: FAILED TO CREATE " + folder_name + "_Backup" + " IN THE CLOUD...";
        }
        return msg;
    }

    public String upload_file(String file_name, int file_size, byte[] bytes){
        String msg = "SUCCESS: " + file_name + " UPLOADED SUCCESSFULLY...";
        try {
            FileOutputStream fileOut = new FileOutputStream(folder_path + file_name);
            fileOut.write(bytes, 0, file_size);
            fileOut.close();
        }
        catch(Exception e){
            msg = "FAILURE: FAILED TO UPLOAD " + file_name + " TO THE CLOUD...";
        }
        return msg;
    }

    public String delete_file(String file_name){
        File to_delete = new File(folder_path + file_name);
        String msg = "SUCCESS: " + file_name + " DELETED SUCCESSFULLY...";
        if (!to_delete.delete()) {
            msg = "FAILURE: FAILED TO DELETE " + file_name + " FROM THE CLOUD...";
        }
        return msg;
    }
}
